#!/usr/bin/env python3

"""Create work logs and search existing logs.

The Work Log program allows the user to create work logs. The user can then
search existing work logs by date, a range of dates, keyword search, task time,
list of usernames, or username search. The user is able to view the work
logs and edit or delete them if wanted.
"""
from collections import OrderedDict
from log import add_log
from login import login
from models import initialize
from search import search_menu
from utils import clear_screen


def main_menu_loop():
    """Show the menu."""
    choice = None

    clear_screen()
    while choice != 'c':
        print("WORK LOG\nWhat would you like to do?")
        for key, value in main_menu_actions.items():
            print("{}) {}".format(key, value.__doc__))
        print("c) Quit program")
        choice = input("\n> ").lower().strip()

        if choice in main_menu_actions:
            clear_screen()
            main_menu_actions[choice]()
        elif choice == 'c':
            continue
        else:
            clear_screen()
            print("That is not a valid selection.")
    clear_screen()
    print("Thank you for using the Work Log program!\n")


main_menu_actions = OrderedDict([
    ('a', add_log),
    ('b', search_menu)
])

if __name__ == '__main__':
    initialize()
    login()
    main_menu_loop()
