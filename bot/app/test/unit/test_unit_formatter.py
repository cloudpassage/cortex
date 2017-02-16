import imp
import os
import sys

module_name = 'donlib'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
donlib = imp.load_module(module_name, fp, pathname, description)

test_item = {"name": "blahblah",
             "id": "noteven",
             "description": "HelloWorld"}
test_list = [test_item]


class TestUnitFormatter:
    def test_unit_formatter_format_list(self):
        assert isinstance(donlib.Formatter.format_list(test_list,
                                                       "issue"), str)

    def test_unit_formatter_format_item(self):
        assert isinstance(donlib.Formatter.format_item(test_item,
                                                       "issue"), str)

    def test_unit_formatter_policy_meta(self):
        assert isinstance(donlib.Formatter.policy_meta(test_item, "ab"), str)
