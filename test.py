import datetime
import unittest

from unittest import mock
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from login import validate_username
from models import initialize
from models import Log
from models import User
from peewee import *
from search import build_datetime_list
from search import get_datetime_list
from search import search_date
from search import search_menu_input
from utils import convert_to_datetime
from utils import format_date
from utils import get_date
from utils import validate_minutes


class UtilsTests(unittest.TestCase):
    def test_convert_to_datetime(self):
        expected = datetime.datetime(2011, 11, 1, 0, 0)
        actual = convert_to_datetime('11/1/2011')
        self.assertEqual(actual, expected)

    def test_format_date(self):
        expected = '11/1/2011'
        actual = format_date('11-1-2011')
        self.assertEqual(actual, expected)

    def test_get_date(self):
        user_input = ['13-1-2011', '11-1-2011']
        with patch('utils.input', side_effect=user_input):
            expected = datetime.datetime(2011, 11, 1, 0, 0)
            actual = get_date("> ")
            self.assertEqual(actual, expected)

    def test_validate_minutes(self):
        user_input = ['abc', '60']
        with patch('utils.input', side_effect=user_input):
            expected = 60
            actual = validate_minutes("> ")
            self.assertEqual(actual, expected)


MODELS = [Log, User]

test_db = SqliteDatabase(':memory:')

class SearchTests(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

        Log.create(username='None',
                   task_date=datetime.datetime(2011, 11, 11, 0, 0),
                   task_title='Test',
                   task_time=60,
                   task_notes='Notes')

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_search_menu_input(self):
        user_input = ['z', 'a']
        with patch('search.input', side_effect=user_input):
            expected = 'a'
            actual = search_menu_input()
            self.assertEqual(actual, expected)

    # def test_search_date(self):
    #     Log.create(username='None', task_date=datetime.datetime(2011, 11, 11, 0, 0), task_title='Test', task_time=60, task_notes='Notes')
    #     user_input = ['2', '1']
    #     with patch('search.input', side_effect=user_input):
    #         expected =
    #         actual = search_date()
    #         self.assertEqual(actual, expected)


    def test_get_datetime_list(self):
        datetimes = [datetime.datetime(2011, 11, 11, 0, 0)]
        expected = "  1) 11/11/2011"
        actual = get_datetime_list(datetimes)
        self.assertEqual(actual, expected)

    def test_build_datetime_list(self):
        expected = [datetime.datetime(2011, 11, 11, 0, 0)]
        actual = build_datetime_list()
        self.assertEqual(actual, expected)


MODELS = [Log, User]

test_db = SqliteDatabase(':memory:')

class ViewerTests(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

        Log.create(username='None',
                   task_date=datetime.datetime(2011, 11, 11, 0, 0),
                   task_title='Test',
                   task_time=60,
                   task_notes='Notes')

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()


    def test_draw_log(self):
        new_viewer = Viewer()
        expected = "Date: 11/11/2011\n" +
                   "Title: Test\n" +
                   "Time Spent: 60\n" +
                   "Notes: Notes\n\n" +
                   "Result 1 of 1"
        actual = self.draw_log()
        self.assertEqual(actual, expected)
#
#     def test_draw_log(self):
#         expected

# class LoginTests(unittest.TestCase):
#     def test_validate_username(self):
#         username = 'test_username'
#         User.create(username = username)
#         expected = username
#         actual = validate_username(username)
#         self.assertEqual(actual, expected)
#         user = User.get().where(User.username=username)
#         user.delete_instance()
#         User.delete_instance().where(username=username)


if __name__ == '__main__':
    initialize()
    unittest.main()
