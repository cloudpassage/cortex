import os
from flake8.api import legacy as f8
import re

heredir = os.path.abspath(os.path.dirname(__file__))
integration_test_directory = os.path.join(heredir, '../integration')
unit_test_directory = os.path.join(heredir, '../unit')
code_directory = os.path.join(heredir, '../../donlib')
app_directory = os.path.join(heredir, '../../')


def flake8_examine(file_location):
    style_guide = f8.get_style_guide()
    result = style_guide.check_files([file_location])
    num_of_errors = result.total_errors
    return num_of_errors


def get_all_py_files(directory):
    pyfiles = []
    pattern = ".*py$"
    for f in os.listdir(directory):
        fullpath = os.path.join(directory, f)
        if (os.path.isfile(fullpath) and re.match(pattern, f)):
            pyfiles.extend([fullpath])
    return pyfiles


class TestF8:
    def test_f8(self):
        dirs_to_test = [code_directory,
                        integration_test_directory,
                        unit_test_directory]
        files_to_test = []
        for d in dirs_to_test:
            files_to_test.extend(get_all_py_files(d))
        for f in files_to_test:
            assert flake8_examine(f) == 0
