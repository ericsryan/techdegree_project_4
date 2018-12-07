"""Create work logs and search existing logsself.

The Work Log program allows the user to create work logs. The user can then
search existing work logs by date, a range of dates, keyword search, task time,
list of usernames, or username search. The user will be able to view the work
logs and edit or delete them if wanted.
"""

from collections import OrderedDict
from log import add_log
from search import search_menu
from utils import clear_screen

def main_menu():
    """Show the menu."""
    choice = None

    while choice != 'c':
        clear_screen()
        print("WORK LOG")
        for key, value in main_menu_actions.items():
            print("{}) {}".format(key, value.__doc__))
        print("c) Quit program")
        choice = input("\n> ").lower().strip()

        if choice in main_menu_actions:
            clear_screen()
            main_menu_actions[choice]()
    clear_screen()
    print("Thank you for using the Work Log program!\n")

main_menu_actions = OrderedDict([
    ('a', add_log),
    ('b', search_menu)
])

if __name__ == '__main__':
    main_menu()
