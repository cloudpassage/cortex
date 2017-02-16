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


class TestIntegrationConfigHelper:
    def instantiate_config_helper(self, monkeypatch):
        monkeypatch.setenv('HALO_API_KEY', api_key_id)
        monkeypatch.setenv('HALO_API_SECRET_KEY', api_secret_key)
        monkeypatch.setenv('HALO_API_HOSTNAME', api_hostname)
        monkeypatch.setenv('HALO_API_PORT', api_port)
        monkeypatch.setenv('SLACK_API_TOKEN', slack_token)
        config_obj = donlib.ConfigHelper()
        return config_obj

    def instantiate_config_helper_insane(self):
        config_obj = donlib.ConfigHelper()
        return config_obj

    def test_config_helper_instantiation(self, monkeypatch):
        config_obj = self.instantiate_config_helper(monkeypatch)
        assert config_obj.halo_api_key == api_key_id
        assert config_obj.halo_api_secret_key == api_secret_key
        assert config_obj.halo_api_host == api_hostname
        assert config_obj.halo_api_port == api_port
        assert config_obj.slack_api_token == slack_token

    def test_config_helper_sane_pass(self, monkeypatch):
        config_obj = self.instantiate_config_helper(monkeypatch)
        assert config_obj.sane()

    def test_config_helper_sane_fail(self):
        config_obj = self.instantiate_config_helper_insane()
        assert not config_obj.sane()
