import cloudpassage
import os
import requests
from formatter import Formatter
from urlparse import urljoin
from utility import Utility as util


class Halo(object):
    """This contains all Halo interaction logic

    Attrubites:
        session (cloudpassage.HaloSession): Halo session object

    """

    def __init__(self, config, health_string, tasks_obj):
        """Initialization only instantiates the session object."""
        self.session = cloudpassage.HaloSession(config.halo_api_key,
                                                config.halo_api_secret_key,
                                                api_host=config.halo_api_host,
                                                api_port=config.halo_api_port,
                                                integration_string=config.ua)
        self.product_version = config.product_version
        self.monitor_events = config.monitor_events
        self.slack_channel = config.slack_channel
        self.health_string = health_string
        self.tasks = tasks_obj
        self.flower_host = config.flower_host
        return

    def credentials_work(self):
        """Attempts to authenticate against Halo API"""
        good = True
        try:
            self.session.authenticate_client()
        except cloudpassage.CloudPassageAuthentication:
            good = False
        return good

    def list_tasks_formatted(self):
        """Gets a formatted list of tasks from Flower"""
        report = "OCTOBOX Tasks:\n"
        celery_url = urljoin(self.flower_host, "api/tasks")
        result = requests.get(celery_url).json()
        try:
            for task in result.items():
                    prefmt = {"id": task[0], "name": task[1]["name"],
                              "args": str(task[1]["args"]),
                              "kwargs": str(task[1]["kwargs"]),
                              "started": util.u_to_8601(task[1]["started"]),
                              "tstamp": util.u_to_8601(task[1]["timestamp"]),
                              "state": task[1]["state"],
                              "exception": str(task[1]["exception"])}
                    report += Formatter.format_item(prefmt, "task")
        except AttributeError as e:  # Empty set will throw AttributeError
            print("Halo.list_tasks_formatted(): AttributeError! %s" % e)
            pass
        return report

    def interrogate(self, query_type, target):
        """Entrypoint for report generation

        This method is where you start for generating reports.  When you add
        a new report this is the second place you configure it, right after
        you set it up in Lexicals.get_message_type().

        Returns a finished report, as a string.
        """
        report = "What do you even MEAN by saying that?  I just can't even.\n"
        if query_type == "server_report":
            report = self.tasks.report_server_formatted.delay(target)
        elif query_type == "group_report":
            report = self.tasks.report_group_formatted.delay(target)
        elif query_type == "ip_report":
            report = self.get_ip_report(target)
        elif query_type == "all_servers":
            report = self.tasks.list_all_servers_formatted.delay()
        elif query_type == "all_groups":
            report = self.tasks.list_all_groups_formatted.delay()
        elif query_type == "group_firewall_report":
            report = self.tasks.report_group_firewall.delay(target)
        elif query_type == "servers_in_group":
            report = self.tasks.servers_in_group_formatted.delay(target)
        elif query_type == "server_compliance_graph":
            report = self.tasks.report_server_scan_graph.delay(target)
        elif query_type == "tasks":
            report = self.list_tasks_formatted()
        elif query_type == "selfie":
            report = Halo.take_selfie()
        elif query_type == "help":
            report = Halo.help_text()
        elif query_type == "version":
            report = Halo.version_info(self.product_version) + "\n"
        elif query_type == "config":
            report = self.running_config()
        elif query_type == "health":
            report = self.health_string
        return(report)

    @classmethod
    def help_text(cls):
        """This is the help output"""
        ret = ("I currently answer these burning questions, " +
               "but only when you address me by name:\n " +
               "\"tell me about server `(server_id|server_name)`\"\n" +
               "\"tell me about ip `ip_address`\"\n" +
               "\"tell me about group `(group_id|group_name)`\"\n" +
               "\"list all servers\"\n" +
               "\"list server groups\"\n" +
               "\"servers in group `(group_id|group_name)`\"\n" +
               "\"group firewall `(group_id|group_name)`\"\n" +
               "\"compliance graph server `(server_id|server_name)`\"\n" +
               "\"version\"\n" +
               "\"tasks\"\n" +
               "\"config\"\n")
        return ret

    @classmethod
    def version_info(cls, product_version):
        return "v%s" % product_version

    def running_config(self):
        if os.getenv("NOSLACK"):
            return "Slack integration is disabled.  CLI access only."
        if self.monitor_events == 'yes':
            events = "Monitoring Halo events"
        else:
            events = "NOT monitoring Halo events"
        retval = "%s\nHalo channel: #%s" % (events, self.slack_channel)
        return retval

    def get_ip_report(self, target):
        """This wraps the report_server_by_id by accepting IP as target"""
        servers = cloudpassage.Server(self.session)
        report = "Unknown IP: \n" + target
        try:
            s_id = servers.list_all(connecting_ip_address=target)[0]["id"]
            report = self.tasks.report_server_formatted(s_id)
        except:
            pass
        return report

    def quarantine_server(self, event):
        server_id = event["server_id"]
        quarantine_group_name = event["quarantine_group"]
        return self.tasks.quarantine_server(server_id, quarantine_group_name)

    def add_ip_to_blocklist(self, ip_address, block_list_name):
        # We trigger a removal job for one hour out.
        self.tasks.remove_ip_from_list.apply_async(args=[ip_address,
                                                         block_list_name],
                                                   countdown=3600)
        return self.tasks.add_ip_to_list.delay(ip_address, block_list_name)

    @classmethod
    def take_selfie(cls):
        selfie_file_name = "selfie.txt"
        heredir = os.path.abspath(os.path.dirname(__file__))
        selfie_full_path = os.path.join(heredir, selfie_file_name)
        with open(selfie_full_path, 'r') as s_file:
            selfie = "```" + s_file.read() + "```"
        return selfie
