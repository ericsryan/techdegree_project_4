"""Tests for the Work Log program."""
import datetime
import mock
import unittest

from peewee import *
from unittest.mock import patch

from log import add_log
from log import get_log_input
from log import get_username
from log import write_log
from login import get_username_input
from login import login
from login import store_username
from models import initialize
from models import Log
from models import User
from search import build_datetime_list
from search import build_username_list
from search import get_logs
from search import get_logs_by_date
from search import get_logs_by_username
from search import get_number_selection
from search import get_range_dates
from search import print_date_menu
from search import print_username_menu
from search import search_date
from search import search_range
from search import search_term
from search import search_time
from search import search_username_list
from search import search_username_term
from utils import convert_to_datetime
from utils import format_date
from utils import get_date
from utils import validate_minutes
from viewer import Viewer


MODELS = [User, Log]

test_db = SqliteDatabase(':memory:')


class LogTests(unittest.TestCase):
    """Tests for log.py."""

    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_get_username(self):
        User.create(username='username')
        expected = 'username'
        actual = get_username()
        self.assertEqual(actual, expected)

    @mock.patch('log.write_log', return_value=True)
    @mock.patch('log.get_log_input', return_value=('0', '1', '2', '3'))
    def test_add_log(self, mock_get_log_input, mock_write_log):
        expected = True
        with patch('log.input', return_value=''):
            actual = add_log()
            self.assertEqual(actual, expected)

    @mock.patch('log.validate_minutes', return_value=60)
    @mock.patch('log.get_date', return_value=datetime.datetime(
                                             2011, 11, 11, 0, 0))
    def test_get_log_input(self, mock_get_date, mock_validate_minutes):
        expected = (datetime.datetime(2011, 11, 11, 0, 0),
                    "Test",
                    60,
                    "Notes")
        with patch('log.input', side_effect=['Test', 'Notes']):
            actual = get_log_input()
            self.assertEqual(actual, expected)

    def test_write_log(self):
        User.create(username='username')
        expected = 'username'
        write_log(datetime.datetime(2011, 11, 11, 0, 0),
                  'Test',
                  60,
                  'Notes'
                  )
        log = Log.select()
        actual = log[0].username
        self.assertEqual(actual, expected)


class LoginTests(unittest.TestCase):
    """Tests for login.py."""

    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_get_username_input(self):
        expected = 'username'
        with patch('login.input', side_effect=['username']):
            actual = get_username_input()
            self.assertEqual(actual, expected)

    def test_login(self):
        expected = 'username'
        with patch('login.input', side_effect=['username', '']):
            actual = login()
            self.assertEqual(actual.username, expected)

    def test_store_username(self):
        expected = 'username'
        with patch('login.input', return_value=''):
            actual = store_username('username')
            self.assertEqual(actual.username, expected)


class ModelsTests(unittest.TestCase):
    """Tests for models.py."""

    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_initialize(self):
        User.create(username='username')
        expected = True
        actual = initialize()
        self.assertEqual(actual, expected)


class SearchTests(unittest.TestCase):
    """Tests for search.py."""

    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        Log.create(username='username',
                   task_date=datetime.datetime(2011, 11, 11, 0, 0),
                   task_title='Test',
                   task_time=60,
                   task_notes='Notes')

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_build_datetime_list(self):
        logs = [Log(task_date=datetime.datetime(2011, 11, 11, 0, 0))]
        expected = [datetime.datetime(2011, 11, 11, 0, 0)]
        actual = build_datetime_list(logs)
        self.assertEqual(actual, expected)

    def test_build_username_list(self):
        expected = ['Adam', 'Bernard', 'Charles']
        logs = [Log(username='Adam'),
                Log(username='Bernard'),
                Log(username='Charles')]
        actual = build_username_list(logs)
        self.assertEqual(actual, expected)

    def test_get_logs(self):
        expected = 'username'
        actual = get_logs()
        self.assertEqual(actual[0].username, expected)

    def test_get_logs_by_date(self):
        expected = datetime.datetime(2011, 11, 11, 0, 0)
        actual = get_logs_by_date(datetime.datetime(2011, 11, 11, 0, 0))
        self.assertEqual(actual[0].task_date, expected)

    def test_get_number_selection(self):
        expected = 1
        with patch('search.input', side_effect=['a', '2', '1']):
            datetime_list = [datetime.datetime(2011, 11, 11, 0, 0)]
            actual = get_number_selection(print_date_menu(datetime_list),
                                          range(1, (len(datetime_list) + 1)))
            self.assertEqual(actual, expected)

    def test_get_range_dates(self):
        expected = (datetime.datetime(2011, 11, 11, 0, 0),
                    datetime.datetime(2012, 11, 11, 0, 0))
        date_input = [datetime.datetime(2011, 11, 11, 0, 0),
                      datetime.datetime(2010, 11, 11, 0, 0),
                      datetime.datetime(2012, 11, 11, 0, 0)]
        with patch('search.get_date', side_effect=date_input):
            actual = get_range_dates()
            self.assertEqual(actual, expected)

    def test_get_logs_by_username(self):
        expected = 'username'
        actual = get_logs_by_username('username')
        self.assertEqual(actual[0].username, expected)

    def test_print_date_menu(self):
        expected = ('For which date would you like to see the logs?\n\n' +
                    '  1) 11/11/2011\n')
        datetime_list = [datetime.datetime(2011, 11, 11, 0, 0)]
        actual = print_date_menu(datetime_list)
        self.assertEqual(actual, expected)

    def test_print_username_menu(self):
        expected = ('Which user\'s logs would you like to view?\n\n' +
                    '  1) Adam\n')
        datetime_list = ['Adam']
        actual = print_username_menu(datetime_list)
        self.assertEqual(actual, expected)

    def test_search_date(self):
        expected = 1
        with patch('search.input', return_value='1'):
            actual = search_date()
            self.assertEqual(actual.select().count(), expected)

    def test_search_range(self):
        expected = datetime.datetime(2011, 11, 11, 0, 0)
        range_dates = (datetime.datetime(2010, 11, 11, 0, 0),
                       datetime.datetime(2012, 11, 11, 0, 0))
        with patch('search.get_range_dates', return_value=range_dates):
            actual = search_range()
            self.assertEqual(actual[0].task_date, expected)

    def test_search_term(self):
        expected = 1
        with patch('search.input', return_value='test'):
            actual = search_term()
            self.assertEqual(actual.select().count(), expected)

    def test_search_time(self):
        expected = 60
        with patch('search.validate_minutes', return_value=60):
            actual = search_time()
            self.assertEqual(actual[0].task_time, expected)

    def test_search_username_list(self):
        expected = 1
        with patch('search.input', return_value='1'):
            actual = search_username_list()
            self.assertEqual(actual.select().count(), expected)

    def test_search_username_term1(self):
        expected = 1
        with patch('search.input', return_value='user'):
            actual = search_username_term()
            self.assertEqual(actual.select().count(), expected)

    def test_search_username_term2(self):
        Log.create(username='username2',
                   task_date=datetime.datetime(2011, 11, 11, 0, 0),
                   task_title='Test',
                   task_time=60,
                   task_notes='Notes'
                   )
        expected = 1
        with patch('search.input', side_effect=['user', '1']):
            actual = search_username_term()
            self.assertEqual(actual.select().count(), expected)

    def test_search_username_term3(self):
        expected = ''
        with patch('search.input', side_effect=['bill', '']):
            actual = search_username_term()
            self.assertEqual(actual, expected)


class UtilsTests(unittest.TestCase):
    """Tests for utils.py."""

    def test_convert_to_datetime(self):
        expected = datetime.datetime(2011, 11, 11, 0, 0)
        actual = convert_to_datetime('11/11/2011')
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


class ViewerTests(unittest.TestCase):
    """Tests for viewer.py."""

    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        Log.create(username='username',
                   task_date=datetime.datetime(2011, 11, 11, 0, 0),
                   task_title='Test',
                   task_time=60,
                   task_notes='Notes')

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_delete_log(self):
        Log.create(username='username',
                   task_date=datetime.datetime(2011, 11, 11, 0, 0),
                   task_title='Test',
                   task_time=60,
                   task_notes='Notes')
        expected = 1
        new_viewer = Viewer(Log.select())
        with patch('viewer.input', side_effect=['n', 'y', '']):
            new_viewer.delete_log()
            new_viewer.delete_log()
            logs = Log.select()
            actual = logs.select().count()
            self.assertEqual(actual, expected)

    def test_draw_log(self):
        log = [Log(username='None',
                   task_date=datetime.datetime(2011, 11, 11, 0, 0),
                   task_title='Test',
                   task_time=60,
                   task_notes='Notes'
                   )]
        new_viewer = Viewer(log)
        expected = ('Logged by: None\n\nDate: 11/11/2011\nTitle: Test\n' +
                    'Time Spent: 60\nNotes: Notes\n\nResult 1 of 1')
        actual = new_viewer.draw_log()
        self.assertEqual(actual, expected)

    @mock.patch('viewer.get_date', return_value=datetime.datetime(
                                                2010, 11, 11, 0, 0))
    def test_edit_log1(self, mock_get_date):
        expected = datetime.datetime(2010, 11, 11, 0, 0)
        new_viewer = Viewer(Log.select())
        with patch('viewer.input', return_value='a'):
            new_viewer.edit_log()
            log = Log.select()
            actual = log[0].task_date
            self.assertEqual(actual, expected)

    def test_edit_log2(self):
        expected = 'Testing'
        new_viewer = Viewer(Log.select())
        with patch('viewer.input', side_effect=['b', 'Testing', '']):
            new_viewer.edit_log()
            log = Log.select()
            actual = log[0].task_title
            self.assertEqual(actual, expected)
        expected = 'More notes'
        new_viewer = Viewer(Log.select())
        with patch('viewer.input', side_effect=['d', 'More notes', '']):
            new_viewer.edit_log()
            log = Log.select()
            actual = log[0].task_notes
            self.assertEqual(actual, expected)

    @mock.patch('viewer.validate_minutes', return_value=45)
    def test_edit_log3(self, mock_validate_minutes):
        expected = 45
        new_viewer = Viewer(Log.select())
        with patch('viewer.input', return_value='c'):
            new_viewer.edit_log()
            log = Log.select()
            actual = log[0].task_time
            self.assertEqual(actual, expected)

    def test_edit_log4(self):
        expected = False
        with patch('viewer.input', return_value='e'):
            new_viewer = Viewer(Log.select())
            actual = new_viewer.edit_log()
            self.assertEqual(actual, expected)

    def test_view_logs(self):
        new_viewer = Viewer([])
        expected = False
        with patch('viewer.input', return_value=''):
            actual = new_viewer.view_logs()
            self.assertEqual(actual, expected)

    def test_view_logs2(self):
        new_viewer = Viewer(Log.select())
        expected = 'eds'
        with patch('viewer.input', return_value='s'):
            new_viewer.view_logs()
            actual = new_viewer.menu_options
            self.assertEqual(actual, expected)

    def test_view_logs3(self):
        Log.create(username='username',
                   task_date=datetime.datetime(2011, 11, 11, 0, 0),
                   task_title='Test',
                   task_time=60,
                   task_notes='Notes')
        new_viewer = Viewer(Log.select())
        expected = 'neds'
        with patch('viewer.input', return_value='s'):
            new_viewer.view_logs()
            actual = new_viewer.menu_options
            self.assertEqual(actual, expected)

    def test_view_logs4(self):
        Log.create(username='username',
                   task_date=datetime.datetime(2011, 11, 11, 0, 0),
                   task_title='Test',
                   task_time=60,
                   task_notes='Notes')
        Log.create(username='username',
                   task_date=datetime.datetime(2011, 11, 11, 0, 0),
                   task_title='Test',
                   task_time=60,
                   task_notes='Notes')
        new_viewer = Viewer(Log.select())
        new_viewer.index += 1
        new_viewer.counter += 1
        expected = 'pneds'
        with patch('viewer.input', return_value='s'):
            new_viewer.view_logs()
            actual = new_viewer.menu_options
            self.assertEqual(actual, expected)

    def test_view_logs5(self):
        Log.create(username='username',
                   task_date=datetime.datetime(2011, 11, 11, 0, 0),
                   task_title='Test',
                   task_time=60,
                   task_notes='Notes')
        Log.create(username='username',
                   task_date=datetime.datetime(2011, 11, 11, 0, 0),
                   task_title='Test',
                   task_time=60,
                   task_notes='Notes')
        new_viewer = Viewer(Log.select())
        new_viewer.index += 2
        new_viewer.counter += 2
        expected = 'peds'
        with patch('viewer.input', return_value='s'):
            new_viewer.view_logs()
            actual = new_viewer.menu_options
            self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
