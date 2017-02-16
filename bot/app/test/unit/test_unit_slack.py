import imp
import os
import sys

module_name = 'donlib'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
donlib = imp.load_module(module_name, fp, pathname, description)

api_key_id = "APIKEYSAMPLE000"
api_secret_key = "APISECRETKEYSAMPLE000"
api_hostname = "api.nonexist.cloudpassage.com"
api_port = "443"
slack_token = "hello-i-am-a-slack-token"

myname = "donbot"
mymessage = {"text": "donbot hi there"}
mymessages = [mymessage]


class TestUnitSlack:
    def instantiate_config_helper(self, monkeypatch):
        monkeypatch.setenv('HALO_API_KEY', api_key_id)
        monkeypatch.setenv('HALO_API_SECRET_KEY', api_secret_key)
        monkeypatch.setenv('HALO_API_HOSTNAME', api_hostname)
        monkeypatch.setenv('HALO_API_PORT', api_port)
        monkeypatch.setenv('SLACK_API_TOKEN', slack_token)
        config_obj = donlib.ConfigHelper()
        return config_obj

    def test_unit_slack_init(self, monkeypatch):
        cfg = self.instantiate_config_helper(monkeypatch)
        assert donlib.Slack(cfg)

    def test_unit_get_my_messages(self):
        assert donlib.Slack.get_my_messages(myname, mymessages)

    def test_unit_message_is_for_me(self):
        assert donlib.Slack.message_is_for_me(myname, mymessage)
