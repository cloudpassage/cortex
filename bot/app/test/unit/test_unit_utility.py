import imp
import os
import sys

module_name = 'donlib'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
donlib = imp.load_module(module_name, fp, pathname, description)


class TestUnitUtility:
    def test_utility_8601_today(self):
        assert isinstance(donlib.Utility.iso8601_today(), str)

    def test_unit_utility_8601_yesterday(self):
        assert isinstance(donlib.Utility.iso8601_yesterday(), str)

    def test_unit_utility_8601_one_month_ago(self):
        assert isinstance(donlib.Utility.iso8601_one_month_ago(), str)

    def test_unit_utility_8601_one_week_ago(self):
        assert isinstance(donlib.Utility.iso8601_one_week_ago(), str)

    def test_unit_utility_8601_now(self):
        assert isinstance(donlib.Utility.iso8601_now(), str)
