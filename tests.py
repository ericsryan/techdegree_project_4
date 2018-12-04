import datetime
from unittest.mock import patch
import unittest

from utils import get_date
from utils import nav_bar


class WorkLogTests(unittest.TestCase):
    def setUp(self):
        pass

    @patch("utils.input")
    def test_get_date(self, mock_input):
        # Normal testcase
        expected_date = datetime.datetime(2011, 11, 11, 0, 0)
        mock_input.return_value = '11-11-2011'
        actual_date = get_date("> ")
        self.assertEqual(actual_date, expected_date)

    def test_nav_bar(self):
        pass


if __name__ == '__main__':
    unittest.main()
