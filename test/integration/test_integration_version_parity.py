import pytest


class TestIntegrationVersionEquality:
    def read_file(self):
        with open('./versions.txt', 'r') as file:
            return file.readlines()

    def test_version_parity(self):
        """This test checks the version of halocelery is consistent
        across don-bot, flower, celeryworker, and scheduler
        """
        content = self.read_file()
        assert content.count(content[0]) == len(content)
