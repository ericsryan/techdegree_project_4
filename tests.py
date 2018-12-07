import datetime
from unittest.mock import patch
import unittest

from utils import get_date
from utils import login
from utils import nav_bar


class UtilsTests(unittest.TestCase):
    def setUp(self):
        pass


    def test_get_date(self):
        # Normal testcase
        user_input = ['13-11-2011', '11-11-2011']
        with patch('utils.input', side_effect=user_input):
            expected_date = datetime.datetime(2011, 11, 11, 0, 0)
            actual_date = get_date("> ")
            self.assertEqual(actual_date, expected_date)


    def test_nav_bar(self):
        expected_nav_bar = '[P]revious | [N]ext | [E]dit | [D]elete | [S]earch Menu'
        actual_nav_bar = nav_bar('pneds')
        self.assertEqual(actual_nav_bar, expected_nav_bar)



if __name__ == '__main__':
    unittest.main()
