from models import Log
from peewee import *
from utils import clear_screen
from utils import get_date
from utils import validate_minutes

def add_log():
    """Add new entry"""
    # Capture input for log fields
    clear_screen()
    task_date = get_date("What is the date of the task? (MM/DD/YYYY): ")
    clear_screen()
    task_title = input("Title of the task: ")
    clear_screen()
    task_time = validate_minutes("Time spent (rounded minutes): ")
    clear_screen()
    task_notes = input("Notes (Optional, you can leave this empty): ")
    # Write log to database
    Log.create(username='None',
               task_date=task_date,
               task_title=task_title,
               task_time=task_time,
               task_notes=task_notes
               )
    clear_screen()
    __ = input("The entry has been added. Press 'Enter' to return to " +
               "the main menu.")
    clear_screen()
