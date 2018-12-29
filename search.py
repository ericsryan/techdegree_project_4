"""Search functions for the Work Log program.

This module provides the functions required to search the existing work logs.
The user can search by exact date, a range of dates, by task time, a search
term, username list, or username search.
"""
import datetime
import itertools

from collections import OrderedDict
from models import Log
from utils import clear_screen
from utils import get_date
from utils import validate_minutes
from viewer import Viewer


def search_menu():
    """Search in existing entries"""
    # Give user menu options
    choice = None
    clear_screen()
    while choice != 'm':
        if Log.select().count() == 0:
            __ = input("There are no logs in the database. " +
                       "Press 'Enter' to return to the main menu. ")
            clear_screen()
            return False
        print("Do you want to search by:")
        # Print docstrings for the search functions
        for key, value in search_menu_actions.items():
            print("{}) {}".format(key, value.__doc__))
        print("\n[M]ain Menu")
        # Capture user menu selection
        choice = input("\n> ").lower().strip()
        # If selection is valid view logs with the selected search function
        if choice in search_menu_actions:
            new_viewer = Viewer(search_menu_actions[choice]())
            new_viewer.view_logs()
        # If selection not on the menu ask for selection again
        elif choice == 'm':
            clear_screen()
            continue
        else:
            clear_screen()
            print("That is not a valid selection.\n")


def get_logs():
    """Retrieve logs from the database."""
    return Log.select()


def get_logs_by_date(date):
    """Retrieve logs from the database that match the provided date."""
    return Log.select().where(Log.task_date == date)


def search_date():
    """Exact date"""
    # Get user selection
    log_dates = build_datetime_list(get_logs())
    menu = print_date_menu(log_dates)
    options = range(1, (len(log_dates) + 1))
    selection = get_number_selection(menu, options)
    # Convert the value to the index value
    selection_index = selection - 1
    # Pull logs with the selected date and return for use in log_viewer
    selected_date = log_dates[selection_index]
    return get_logs_by_date(selected_date)


def get_number_selection(menu, options):
    """Get valid selection from user."""
    clear_screen()
    while True:
        print(menu)
        try:
            selection = int(input("> ").strip())
        except ValueError:
            clear_screen()
            print("That is not a valid selection")
            continue
        if selection in options:
            return selection
        else:
            clear_screen()
            print("That is not a valid selection.")
            continue


def build_datetime_list(logs):
    """Create list of unique datetimes oredered from earliest to latest."""
    date_list = []
    # Pull the datetimes from the database
    for log in logs:
        # Write new datetimes to the list of datetimes
        if log.task_date not in date_list:
            date_list.append(log.task_date)
    return date_list


def print_date_menu(datetimes):
    """Print menu with list of available datetimes."""
    counter = itertools.count(start=1)
    date_list = "For which date would you like to see the logs?\n\n"
    for date in datetimes:
        # Print a numbered list of dates (  1) MM/DD/YYY)
        date_list += ("  " + str(next(counter)) + ") " +
                      datetime.datetime.strftime(date, '%m/%d/%Y') + "\n")
    return date_list


def search_range():
    """Range of dates"""
    # Get dates for Range
    range_dates = get_range_dates()
    # Pull logs that fall into the date range
    return Log.select().where(Log.task_date >= range_dates[0] and
                              Log.task_date <= range_dates[1])


def get_range_dates():
    """Get dates from the user to search by date range."""
    clear_screen()
    print("What beggining date would you like to use for the range? " +
          "(MM/DD/YYYY)\n")
    begin_range = get_date("> ")
    clear_screen()
    while True:
        print("What ending date would you like to use for the range? " +
              "(MM/DD/YYYY)\n")
        end_range = get_date("> ")
        if begin_range > end_range:
            clear_screen()
            print("The ending date must be after {}.".format(
                  datetime.datetime.strftime(begin_range, '%m/%d/%Y')))
        else:
            return begin_range, end_range


def search_time():
    """Time spent"""
    clear_screen()
    minutes = validate_minutes("Enter the amount of time for the " +
                               "logs that you would like to see.\n> ")
    return Log.select().where(Log.task_time == minutes)


def search_term():
    """Search by term"""
    clear_screen()
    search_term = '%' + input("Enter the term that you would like to use " +
                              "to search the logs.\n> ") + '%'
    search_logs = Log.select().where(Log.task_title ** search_term |
                                     Log.task_notes ** search_term)
    return search_logs


def search_username_list():
    """Username list"""
    # Get user selection
    usernames = build_username_list(get_logs())
    menu = print_username_menu(usernames)
    options = range(1, (len(usernames) + 1))
    selection = get_number_selection(menu, options)
    # Convert the value to the index value
    selection_index = selection - 1
    # Pull logs with the selected date and return for use in log_viewer
    selected_username = usernames[selection_index]
    return get_logs_by_username(selected_username)


def get_logs_by_username(username):
    """Retrieve logs from the database that match the provided username."""
    return Log.select().where(Log.username == username)


def build_username_list(logs):
    """Create list of unique usernames."""
    username_list = []
    # Pull the datetimes from the database
    for log in logs:
        # Write new datetimes to the list of datetimes
        if log.username not in username_list:
            username_list.append(log.username)
    return username_list


def print_username_menu(usernames):
    """Print menu with list of available datetimes."""
    counter = itertools.count(start=1)
    username_list = "Which user's logs would you like to view?\n\n"
    for username in usernames:
        # Print a numbered list of usernames (  1) User)
        username_list += "  " + str(next(counter)) + ") " + username + "\n"
    return username_list


def search_username_term():
    """Lookup username"""
    clear_screen()
    username = '%' + input("Enter the user's name that you would like to " +
                           "use to search the logs.\n> ") + '%'
    matching_usernames = build_username_list(Log.select().where(Log.username **
                                                                username))
    if len(matching_usernames) > 1:
        print("There is more than one user with that name. ")
        menu = print_username_menu(matching_usernames)
        options = range(1, (len(matching_usernames) + 1))
        selection = get_number_selection(menu, options)
        # Convert the value to the index value
        selection_index = selection - 1
        # Pull logs with the selected name and return for use in log_viewer
        selected_username = matching_usernames[selection_index]
        return get_logs_by_username(selected_username)
    elif len(matching_usernames) == 1:
        return Log.select().where(Log.username ** username)
    else:
        return ''


search_menu_actions = OrderedDict([
    ('a', search_date),
    ('b', search_range),
    ('c', search_time),
    ('d', search_term),
    ('e', search_username_list),
    ('f', search_username_term)
])
