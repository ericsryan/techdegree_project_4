import datetime
import os

from model import Log
from model import User
from peewee import *


db = SqliteDatabase('logs.db')

def clear_screen():
    """Clear screen for better readability.

    >>> clear_screen()
    >>>

    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_date(question):
    """Validate input and return date as a datetime object."""
    while True:
        formatted_date = ''
        try:
            date_input = input(question)
            for character in date_input:
                if character == '-':
                    formatted_date += '/'
                else:
                    formatted_date += character
            formatted_date = datetime.datetime.strptime(formatted_date,
                                                        '%m/%d/%Y')
        except ValueError:
            clear_screen()
            print("The date was not formatted correctly. Please try again.")
        else:
            break
    return formatted_date


def initialize():
    """Create the database and table if they do not exist."""
    db.connect()
    db.create_tables([Log, User], safe=True)


def login():
    """Login with username or sign up for a new username."""
    clear_screen()
    print("Enter your username or press 'Enter' to register new username")
    username = input("> ")
    while True:
        if username:
            try:
                clear_screen()
                User.get(User.username == username)
                next_screen = input("{}, welcome ".format(username) +
                                    "to the Work Log program. " +
                                    "Press 'Enter' to continue. ")
                break
            except Exception:
                clear_screen()
                print("That username does not exist. "
                      "Would you like to register it now? Y/N")
                selection = input("> ").lower().strip()
                if selection == 'y':
                    clear_screen()
                    User.create(username=username)
                    next_screen = input("{} is ".format(username) +
                                        "now your username. " +
                                        "Press 'Enter' to continue. ")
                    break
                elif selection == 'n':
                    clear_screen()
                    continue
        else:
            clear_screen()
            while True:
                try:
                    if username:
                        clear_screen()
                        break
                    else:
                        print("Enter the username that you would like to use.")
                        username = input("> ")
                        User.create(username=username)
                        break
                except IntegrityError:
                    clear_screen()
                    while True:
                        print("That username is already in use. " +
                              "Would you like to login with\nthis username? " +
                              "Press 'Enter' to continue with this username " +
                              "or\nenter the new username you would like " +
                              "to register.")
                        continue_login = input("> ")
                        if continue_login == '':
                            break
                        else:
                            try:
                                username = continue_login
                                User.create(username=username)
                                break
                            except IntegrityError:
                                clear_screen()
                                continue
    return username



def nav_bar(options):
    """Generate a navigation bar to be used while viewing logs."""
    menu_options = [
        ('p', '[P]revious'),
        ('n', '[N]ext'),
        ('e', '[E]dit'),
        ('d', '[D]elete'),
        ('s', '[S]earch Menu'),
        ('m', '[M]ain Menu')
        ]
    bar = []
    for option in menu_options:
        if option[0] in options:
            bar.append(option[1])
            bar.append(' | ')
    del bar[-1]
    return ''.join(bar)
