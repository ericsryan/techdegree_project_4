from model import Log
from model import User
from utils import clear_screen


def login_menu():
    clear_screen()
    while True:
        login_screen()
        login_input = input("> ")
        if login_input.lower() == 'r':
            clear_screen()
            username = input("Enter the username that you would like to use." +
                             "\n\n> ")
            register(username)
        elif login_input.lower() == 'q':
        else:
            login(login_input)


def login(username):
    """Varify username is in the database and return the username."""
    try:
        User.get(User.username==username)
        clear_screen()
        print("{}, welcome to the Work Log program. ".format(username) +
              "Press 'Enter' to continue.")
        __ = input("")
        return username
    except Exception:
        clear_screen()
        print("{} is not a registered username. ".format(username) +
              "Press 'Enter' to return to the login screen.")
        __ = input("")
        return False

def register(username):
    """Register and return username."""
    try:
        User.create(username=username)
        clear_screen()
        print("{}, welcome to the Work Log program. ".format(username) +
              "Press 'Enter' to continue.")
        __ = input("")
        return username
    except Exception:
        clear_screen()
        print("{} is already a registered username. ".format(username) +
              "Would you like to login using this username? Y/N: ")
        register_selection = input("> ").lower().strip()
        if register_selection == 'y':
            login(username)
        elif register_selection == 'n':
            clear_screen()
            __ = input("You will now be returned to the login menu.\n" +
                       "Press 'Enter' to continue.")
            return False
