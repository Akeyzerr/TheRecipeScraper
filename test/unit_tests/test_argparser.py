import sys
import unittest

from modules.settings import ArgParserSettings

try:
    from unittest.mock import patch as mock_argv
except ImportError:
    from mock import patch as mock_argv

from modules.argparser import ArgParser
from project_exceptions.argParser_exceptions import *


class ArgParserTests(unittest.TestCase):
    test_settings = ArgParserSettings()

    @mock_argv.object(sys, 'argv', [sys.argv[0], '-n', 5])
    def test_dishes_arg(self):
        # TODO: Initial test comment
        test_argp = ArgParser(settings=self.test_settings, mock_args=sys.argv)
        res = test_argp.count
        self.assertEqual(res, 5)

    @mock_argv.object(sys, 'argv', [sys.argv[0], '-n'])
    def test_dishes_arg_no_param_error(self):
        # TODO: Initial test comment
        with self.assertRaises(RequiredArgParamException):
            ArgParser(settings=self.test_settings, mock_args=sys.argv)

    def test_dishes_arg_no_n_param_error(self):
        # TODO: Initial test comment
        with self.assertRaises(RequiredArgException):
            ArgParser(settings=self.test_settings, mock_args=sys.argv)


if __name__ == '__main__':
    unittest.main()
