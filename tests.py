import datetime
import mock
import unittest

from work_log import get_date


class UtilsTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_date(self):
        self.assertEqual(get_date("> "),
                         datetime.datetime(2011, 11, 11, 0, 0))


if __name__ == '__main__':
    unittest.main()
