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
api_hostname = "api.cloudpassage.com"
api_port = "443"
slack_token = "hello-i-am-a-slack-token"


class TestUnitHalo:
    def instantiate_config_helper(self, monkeypatch):
        monkeypatch.setenv('HALO_API_KEY', api_key_id)
        monkeypatch.setenv('HALO_API_SECRET_KEY', api_secret_key)
        monkeypatch.setenv('HALO_API_HOSTNAME', api_hostname)
        monkeypatch.setenv('HALO_API_PORT', api_port)
        monkeypatch.setenv('SLACK_API_TOKEN', slack_token)
        config_obj = donlib.ConfigHelper()
        return config_obj

    def test_unit_halo_init(self, monkeypatch):
        cfg = self.instantiate_config_helper(monkeypatch)
        assert donlib.Halo(cfg, "", "")

    def test_unit_help_text(self):
        assert donlib.Halo.help_text()

    def test_unit_selfie(self):
        assert donlib.Halo.take_selfie()

    def test_unit_interrogate_help_text(self, monkeypatch):
        cfg = self.instantiate_config_helper(monkeypatch)
        h_obj = donlib.Halo(cfg, "", "")
        assert h_obj.interrogate("help", "help")

    def test_unit_interrogate_selfie(self, monkeypatch):
        cfg = self.instantiate_config_helper(monkeypatch)
        h_obj = donlib.Halo(cfg, "", "")
        assert h_obj.interrogate("selfie", "selfie")

    def test_unit_credentials_work(self, monkeypatch):
        cfg = self.instantiate_config_helper(monkeypatch)
        h_obj = donlib.Halo(cfg, "", "")
        assert h_obj.credentials_work() is False
