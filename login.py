# Prompt user for thier username or ask if they would like to register a new
# one

# If user enters username varify that it is in the database

# If user registers new name varify that it is not in the database

# Return the username and use it for entries made during the session
from models import User
from utils import clear_screen


def get_username():
    clear_screen()
    while True:
        username = input("Enter your username or enter " +
                         "'R' to register a new one.\n> " )
        if username.lower().strip() == 'r':
            new_username = input("Enter the usename you would like to " +
                                 "register.\n> ")
            username = register_username(new_username)
            return username
        else:
            username = validate_username(username)
            return username
        if not username:
            continue


def validate_username(username):
    try:
        User.get(User.username == username)
        clear_screen()
        print("{}, welcome to the Work Log program.".format(username))
        return username
    except IndexError:
        clear_screen()
        register = input("That is not a registered username. Would you like " +
                         "to register it now? Y/N\n> ").lower().strip()
        if register == 'y':
            register_username(username)
            return username
        else:
            clear_screen()
            __ = input("Press 'Enter' to return the the login screen. ")
            return False

def register_username(username):
    try:
        User.create(username = username)
    except IntegrityError:
        login = input("That username has already been registered. " +
                      "Would you like to login with that username? Y/N\n> ")
        if login.lower().strip() == 'y':
            return username
        else:
            clear_screen()
            __ = input("Press 'Enter' to return the the login screen. ")
            return False
