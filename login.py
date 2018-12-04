"""Login to the Work Log program.

The user will be prompted for their username or asked to register a new
username. The supplied username will be varified against a database. The login
program will then return the varified username.
"""

from peewee import *

db = SqliteDatabase('login.db')

class User(Model):
    username = CharField(max_length=100, unique=True)

    class Meta:
        database = db


def initialize():
    """Create the database and table if they do not exist."""
    db.connect()
    db.create_tables([Log, User], safe=True)


def check_username(username):
    """Check that the username is in the database."""
    while True:
        try:
            clear_screen()
            User.get(User.username == username)
            __ = input("{}, welcome ".format(username) +
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


def register_username(username):
    """Add new username to the database."""
    try:
        User.create(username=username)
        print("{}, your username has been registered.".format(username))
        return True
    except IntegrityError:
        print("The username, {}, is already in use.".format(username))
        return False

def login_menu():
    """Get username from the user and return the varified username."""
    while True:
        print("Enter your username or enter " +
              "'R' to register a new username."
              )
        username = input("> ").lower().strip()
        if username == 'r':
            print("Enter the username that you would like to register.")
            new_username = input("> ").lower().strip()
            register_username()


if __name__ == '__main__':
    get_username()
