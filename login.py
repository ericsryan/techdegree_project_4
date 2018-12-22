"""Login utility for the Work Log program."""
from models import User
from utils import clear_screen


def login():
    """Logic for the login screen."""
    clear_screen()
    username = get_username_input()
    user = store_username(username)
    return user


def get_username_input():
    """Get username input from the user."""
    username = input("Enter the username that you would like " +
                     "to use for this session.\n> ")
    return username


def store_username(username):
    """Add the username to the database."""
    user = User.create(username=username)
    clear_screen()
    __ = input("{}, welcome to the Work Log program. ".format(username) +
               "Press 'Enter' to continue. ")
    return user
