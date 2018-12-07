"""Enter or edit logs in the Work Log program.

This file contains functions to create and edit work logs.
"""

import datetime

from model import Log
from peewee import *
from utils import clear_screen
from utils import get_date


def add_log():
    """Add new entry"""
    clear_screen()
    task_date = get_date("Task date. (MM/DD/YYYY): ")
    clear_screen()
    task_title = input("Title of the task: ")
    clear_screen()
    task_time = int(input("Time spent (rounded minutes): "))
    clear_screen()
    task_notes = input("Notes (Optional, you can leave this empty): ")
    if task_notes == '':
        task_notes = 'None'
    clear_screen()
    Log.create(username=username,
               task_date=task_date,
               task_title=task_title,
               task_time=task_time,
               task_notes=task_notes)
    next_screen = input("The entry has been added. " +
                        "Press enter to return to the main menu")
    clear_screen()


def edit_log(log):
    """Edit the selected work log."""
    while True:
        clear_screen()
        print("Which field would you like to edit?\n\n" +
              "  a) Date\n" +
              "  b) Title\n" +
              "  c) Time\n" +
              "  d) Notes\n")
        selection = input("> ").lower().strip()
        if selection not in 'abcd':
            print("That is not a valid selection.\n")
            continue
        elif selection == 'a':
            clear_screen()
            print("Original Date: " +
                  datetime.datetime.strftime(log.task_date, '%m/%d/%Y') +
                  "\n\nWhat would you like the date to be?\n")
            new_date = get_date("> ")
            log.update(task_date=new_date).execute()
        elif selection == 'b':
            clear_screen()
            print("Original Title: " + log.task_title +
                  "\n\nWhat would you like the title to be?\n")
            new_title = input("> ")
            log.update(task_title=new_title).execute()
        elif selection == 'c':
            clear_screen()
            print("Original Time: " + str(log.task_time) +
                  "\n\nWhat would you like the time to be?\n")
            new_time = input("> ")
            log.update(task_time=new_time).execute()
        elif selection == 'd':
            clear_screen()
            print("Original Notes: " + log.task_notes +
                  "\n\nWhat would you like the notes to be?\n")
            new_notes = input("> ")
            log.update(task_notes=new_notes).execute()
        break
