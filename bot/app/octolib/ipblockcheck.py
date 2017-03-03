import os
import re
import yaml


class IpBlockCheck(object):
    here_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(here_dir, "../../octo_conf.yml")

    def __init__(self):
        self.ip_zone_name = ""
        self.trigger_events = []
        self.trigger_only_on_critical = True
        self.set_ipblockcheck_config()
        self.validate_config()

    def should_block_ip(self, event):
        if (self.trigger_only_on_critical == True and
            event["critical"] is False):
            pass
        elif event["type"] in self.trigger_events:
            return IpBlockCheck.extract_ip_from_event(event)
        return False

    @classmethod
    def extract_ip_from_event(cls, event):
        rxen = [r'from\s(?P<addy>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\sport',
                r'(?P<addy>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})']
        message = event["message"]
        for rx in rxen:
            m = re.search(rx, message)
            if m.group("addy"):
                return m.group("addy")
        return None


    def set_ipblockcheck_config(self):
        with open(IpBlockCheck.config_file, 'r') as config:
            ipblock_conf = yaml.load(config)["ipblocker"]
        self.ip_zone_name = ipblock_conf["ip_zone_name"]
        self.trigger_events = ipblock_conf["trigger_events"]
        self.trigger_only_on_critical = ipblock_conf["trigger_only_on_critical"]

    def validate_config(self):
        ref = {"should_be_lists": [self.trigger_events],
               "should_be_bool": [self.trigger_only_on_critical],
               "should_be_string": [self.ip_zone_name]}
        for v in ref["should_be_lists"]:
            if not isinstance(v, list):
                msg = "%s is not the correct type!  Should be a list!" % str(v)
                raise ValueError(msg)
        for v in ref["should_be_bool"]:
            if not isinstance(v, bool):
                msg = "%s is not the correct type!  Should be a bool!" % str(v)
                raise ValueError(msg)
        for v in ref["should_be_string"]:
            if not isinstance(v, str):
                msg = "%s is not the correct type!  Should be string!" % str(v)
                raise ValueError(msg)
