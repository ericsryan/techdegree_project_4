import datetime
import itertools

from collections import OrderedDict
from models import Log
from utils import clear_screen
from viewer import Viewer


def search_menu_input():
    """Search in existing entries"""
    # Give user menu options
    choice = None
    clear_screen()
    while choice != 'm':
        if Log.select().count() == 0:
            __ = input("There are no logs in the database. " +
                       "Press 'Enter' to return to the main menu. ")
            break
        print("Do you want to search by:")
        # Print docstrings for the search functions
        for key, value in search_menu_actions.items():
            print("{}) {}".format(key, value.__doc__))
        print("\n[M]ain Menu")
        # Capture user menu selection
        choice = input("\n> ").lower().strip()
        # If selection is valid view logs with the selected search function
        if choice in search_menu_actions:
            return choice
        # If selection not on the menu ask for selection again
        else:
            clear_screen()
            print("That is not a valid selection.\n")


def run_search_menu(choice):
    """Search in existing entries"""
    clear_screen()
    new_viewer = Viewer(search_menu_actions[choice]())
    new_viewer.log_viewer()

def search_date():
    """Exact date"""
    # Create list of unique datetimes to create the selection list
    datetime_list = build_datetime_list()
    # Print list of work log dates
    clear_screen()
    while True:
        print("For which date would you like to see the work logs?\n")
        print(datetime_list)
        # Get user selection
        date_selection = input("\n> ")
        # Convert the value to the index value
        try:
            date_selection = int(date_selection) - 1
            # If the selection is not in the list ask user for a new selection
            if date_selection not in range(0, (len(datetime_list))):
                raise ValueError
        # If input was not a number character ask user for a new selection
        except ValueError:
            clear_screen()
            print("Sorry, that is not a valid selection.")
            continue
        # Pull logs with the selected date and return for use in log_viewer
        else:
            logs = Log.select().where(Log.task_date==
                                      datetime_list[date_selection])
            break
    return logs


def build_datetime_list():
    """Create list of unique datetimes oredered from earliest to latest."""
    date_list = []
    # Pull the datetimes from the database
    logs = Log.select()
    logs.order_by(Log.task_date.desc())
    for log in logs:
        # Write new datetimes to the list of datetimes
        if log.task_date not in date_list:
            date_list.append(log.task_date)
    return date_list


def get_datetime_list(datetimes):
    """Print list of available datetimes."""
    counter = itertools.count(start=1)
    for date in datetimes:
        # Print a numbered list of dates (  1) MM/DD/YYY)
        return ("  " + str(next(counter)) + ") " +
              datetime.datetime.strftime(date, '%m/%d/%Y'))



def search_range():
    """Range of dates"""
    pass


def search_time():
    """Time spent"""
    pass


def search_term():
    """Search by term"""
    pass


def search_username_list():
    """Username list"""
    pass


def search_username_term():
    """Lookup username"""
    pass


search_menu_actions = OrderedDict([
    ('a', search_date),
    ('b', search_range),
    ('c', search_time),
    ('d', search_term),
    ('e', search_username_list),
    ('f', search_username_term)
])
