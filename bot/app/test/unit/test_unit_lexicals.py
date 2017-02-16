import imp
import os
import sys

module_name = 'donlib'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
donlib = imp.load_module(module_name, fp, pathname, description)


class TestUnitLexicals:
    def test_unit_lexical_parse(self):
        message = {"text": "You'll never make anything out of this message"}
        result_1, result_2 = donlib.Lexicals.parse(message)
        assert result_1 == "unknown"

    def test_unit_lexical_get_message_type_server_report_1(self):
        message = "donbot tell me about server xyz"
        report_type = "server_report"
        r_type = donlib.Lexicals.get_message_type(message)
        assert r_type == report_type

    def test_unit_lexical_get_message_type_server_report_2(self):
        message = "donbot tell me about server \"xyz zyx\" "
        report_type = "server_report"
        r_type = donlib.Lexicals.get_message_type(message)
        assert r_type == report_type

    def test_unit_lexical_get_message_type_group_report_1(self):
        message = "donbot tell me about group xyz"
        report_type = "group_report"
        r_type = donlib.Lexicals.get_message_type(message)
        assert r_type == report_type

    def test_unit_lexical_get_message_type_group_report_2(self):
        message = "donbot tell me about group \"xyz zyx\" "
        report_type = "group_report"
        r_type = donlib.Lexicals.get_message_type(message)
        assert r_type == report_type

    def test_unit_lexical_get_message_type_ip_report(self):
        message = "donbot tell me about ip 1.2.3.4"
        report_type = "ip_report"
        r_type = donlib.Lexicals.get_message_type(message)
        assert r_type == report_type

    def test_unit_lexical_get_message_type_all_servers(self):
        message = "donbot list all servers"
        report_type = "all_servers"
        r_type = donlib.Lexicals.get_message_type(message)
        assert r_type == report_type

    def test_unit_lexical_get_message_type_all_server_groups(self):
        message = "donbot list server groups"
        report_type = "all_groups"
        r_type = donlib.Lexicals.get_message_type(message)
        assert r_type == report_type

    def test_unit_lexical_get_message_type_servers_in_group_report_1(self):
        message = "donbot tell me about servers in group xyz"
        report_type = "servers_in_group"
        r_type = donlib.Lexicals.get_message_type(message)
        assert r_type == report_type

    def test_unit_lexical_get_message_type_serers_in_group_report_2(self):
        message = "donbot tell me about servers in group \"xyz zyx\" "
        report_type = "servers_in_group"
        r_type = donlib.Lexicals.get_message_type(message)
        assert r_type == report_type

    def test_unit_lexical_get_message_type_selfie(self):
        message = "donbot selfie"
        report_type = "selfie"
        r_type = donlib.Lexicals.get_message_type(message)
        assert r_type == report_type

    def test_unit_lexical_get_message_type_help(self):
        message = "donbot help"
        report_type = "help"
        r_type = donlib.Lexicals.get_message_type(message)
        assert r_type == report_type

    def test_unit_lexical_get_single_quoted_value(self):
        message = 'test message "with a target"'
        expected = "with a target"
        assert donlib.Lexicals.get_target(message) == expected

    def test_unit_lexical_get_single_quoted_value_fail(self):
        message = 'test message with no valid target.'
        expected = ""
        assert donlib.Lexicals.get_target(message) == expected

    def test_unit_lexical_get_last_unquoted_value(self):
        message = 'test message with a target'
        expected = "target"
        assert donlib.Lexicals.get_target(message) == expected

    def test_unit_lexical_get_last_unquoted_value_fail(self):
        message = 'test message with no target '
        expected = ""
        assert donlib.Lexicals.get_target(message) == expected

    def test_unit_lexical_get_version(self):
        message = 'donbot version'
        expected = "version"
        assert donlib.Lexicals.get_target(message) == expected

    def test_unit_lexical_get_config(self):
        message = 'donbot config'
        expected = "config"
        assert donlib.Lexicals.get_target(message) == expected

    def test_unit_lexical_get_health(self):
        message = 'donbot health'
        expected = "health"
        assert donlib.Lexicals.get_target(message) == expected

    def test_unit_lexical_get_tasks(self):
        message = 'donbot tasks'
        expected = "tasks"
        assert donlib.Lexicals.get_target(message) == expected

    def test_unit_lexical_firewall_report(self):
        message = 'donbot group firewall xyz'
        expected = "group_firewall_report"
        assert donlib.Lexicals.get_message_type(message) == expected

    def test_unit_lexical_firewall_report_target(self):
        message = 'donbot group firewall xyz'
        expected = "xyz"
        assert donlib.Lexicals.get_target(message) == expected
