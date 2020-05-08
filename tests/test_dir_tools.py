import os, unittest

from unittest import mock

from mock import patch
from goji.dir_tools import make_empty_git_dir 

class MockingTestTestCase(unittest.TestCase):
    @patch('builtins.open')
    @patch('goji.dir_tools.os.makedirs')
    def test_make_empty_git_dir(self, makedirs, builtin_open):
        file_mock = mock.Mock()
        builtin_open.return_value = file_mock

        make_empty_git_dir("foo")

        makedirs.assert_called_with("foo")
        builtin_open.assert_called_with(os.path.join("foo", ".gitkeep"), "w+")
        file_mock.close.assert_called()
