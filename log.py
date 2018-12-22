"""Log menu and and writer for the Work Log program."""
from models import Log
from models import User
from peewee import *
from utils import clear_screen
from utils import get_date
from utils import validate_minutes


def add_log():
    """Add new entry"""
    log = get_log_input()
    write_log(log[0], log[1], log[2], log[3])
    clear_screen()
    __ = input("The entry has been added. Press 'Enter' " +
               "to return to the main menu. ")
    clear_screen()
    return True


def get_log_input():
    """Get log information from the user."""
    clear_screen()
    task_date = get_date("What is the date of the task? (MM/DD/YYYY): ")
    clear_screen()
    task_title = input("Title of the task: ")
    clear_screen()
    task_time = validate_minutes("Time spent (rounded minutes): ")
    clear_screen()
    task_notes = input("Notes (Optional, you can leave this empty): ")
    return task_date, task_title, task_time, task_notes


def get_username():
    """Retrieve the username from the database."""
    user = User.select()
    return user[0].username


def write_log(date, title, time, notes):
    """Write the work log to the database."""
    username = get_username()
    Log.create(username=username,
               task_date=date,
               task_title=title,
               task_time=time,
               task_notes=notes)
