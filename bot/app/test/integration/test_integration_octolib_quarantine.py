import imp
import os
import pytest
import sys

module_name = 'octolib'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
octolib = imp.load_module(module_name, fp, pathname, description)

safe_event = {"server_group_name": "NOTME",
              "type": "NOT_A_BAD_TYPE",
              "critical": True}

quar_event = {"server_group_name": "q-test",
              "type": "lids_rule_failed",
              "critical": True}


class TestIntegrationOctolibQuarantine:
    def instantiate_octolib_quarantine(self):
        q_obj = octolib.Quarantine()
        return q_obj

    def test_instantiate_octolib_quarantine(self):
        assert self.instantiate_octolib_quarantine()

    def test_trigger_validation_fail(self):
        q = self.instantiate_octolib_quarantine()
        with pytest.raises(ValueError):
            q.trigger_events = 123
            q.validate_config()
        with pytest.raises(ValueError):
            q.trigger_group_names = "invalidus maximus"
            q.validate_config()
        with pytest.raises(ValueError):
            q.quarantine_group_name = ["invalidus minimus"]
            q.validate_config()
        with pytest.raises(ValueError):
            q.trigger_only_on_critical = "YAS"
            q.validate_config()

    def test_quarantine_event_trigger(self):
        q_grp = "Quarantine"
        q = self.instantiate_octolib_quarantine()
        assert q.should_quarantine(quar_event)["quarantine_group"] == q_grp

    def test_quarantine_event_no_trigger(self):
        q = self.instantiate_octolib_quarantine()
        assert q.should_quarantine(safe_event) is False
