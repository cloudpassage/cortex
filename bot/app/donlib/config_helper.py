import os
import re


class ConfigHelper(object):
    """This class contains all application configuration variables.

    All configuration variables in this class are derived from environment
    variables.

    Attributes:
        halo_api_key (str): Halo API key, sometimes referred to as 'key id'
        halo_api_secret_key (str): Halo API secret associated with halo_api_key
        halo_api_hostname (str): Hostname for Halo API
        halo_api_port (str): Halo API port
        slack_api_token (str): Slack API token
        slack_username (str): Donbot's user name (purely cosmetic)
        slack_icon (str): Donbot's avatar

    """
    def __init__(self):
        self.halo_api_key = os.getenv("HALO_API_KEY", "HARDSTOP")
        self.halo_api_secret_key = os.getenv("HALO_API_SECRET_KEY", "HARDSTOP")
        self.halo_api_host = os.getenv("HALO_API_HOSTNAME", "HARDSTOP")
        self.halo_api_port = os.getenv("HALO_API_PORT", "HARDSTOP")
        self.slack_api_token = os.getenv("SLACK_API_TOKEN", "HARDSTOP")
        self.slack_username = os.getenv("SLACK_USERNAME", "donbot")
        self.slack_icon_url = os.getenv("SLACK_ICON_URL", "")
        self.slack_channel = os.getenv("SLACK_CHANNEL", "halo")
        self.monitor_events = os.getenv("MONITOR_EVENTS", "no")
        self.flower_host = os.getenv("FLOWER_HOST")
        self.max_threads = 5  # Max thresds to be used by event collector
        self.halo_batch_size = 5  # Pagination depth for event collector
        self.ua = ConfigHelper.get_ua_string()
        self.product_version = ConfigHelper.get_product_version()

    @classmethod
    def get_ua_string(cls):
        product = "HaloSlackbot"
        version = ConfigHelper.get_product_version()
        ua_string = product + "/" + version
        return ua_string

    @classmethod
    def get_product_version(cls):
        init = open(os.path.join(os.path.dirname(__file__),
                    "__init__.py")).read()
        rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
        version = rx_compiled.search(init).group(1)
        return version

    def sane(self):
        """Tests to make sure that required config items are set.

        Returns:
            True if everything is OK, False if otherwise

        """
        sanity = True
        template = "Required configuration variable {0} is not set!"
        critical_vars = {"HALO_API_KEY": self.halo_api_key,
                         "HALO_API_SECRET": self.halo_api_secret_key,
                         "HALO_API_HOSTNAME": self.halo_api_host,
                         "HALO_API_PORT": self.halo_api_port,
                         "SLACK_API_TOKEN": self.slack_api_token}
        for name, varval in critical_vars.items():
            if varval == "HARDSTOP":
                sanity = False
                print(template.format(name))
        return sanity
