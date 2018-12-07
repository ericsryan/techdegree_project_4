#!/usr/bin/env python3
"""Enter work logs and search existing logs.

Users have the option of entering a work log or searching existing logs. They
also have the option of editing or deleteing existing entries.
"""

from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('logs.db')

class Log(Model):
    username = CharField(max_length=100)
    task_date = DateTimeField(default=datetime.datetime.now)
    task_title = CharField(max_length=255)
    task_time = IntegerField()
    task_notes = TextField()

    class Meta:
        database = db

class User(Model):
    username = CharField(max_length=100, unique=True)

    class Meta:
        database = db

###########
#Utilities#
###########

def clear_screen():
    """Clear screen for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_date(question):
    """Validate and return date input."""
    while True:
        # Format date_input for consistancy and flexibility
        # Validate date input
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
                                User.create(username=username)
                                break
                            except IntegrityError:
                                clear_screen()
                                continue
    return username



def nav_bar(options):
    """Generate a navigation bar to be used while viewing logs."""
    d = '[D]elete'
    e = '[E]dit'
    m = '[M]ain Menu'
    n = '[N]ext'
    p = '[P]revious'
    s = '[S]earch Menu'
    bar = []
    for letter in options:
        bar.append(eval(letter))
        bar.append(' | ')
    del bar[-1]
    print(''.join(bar))

#######
#Menus#
#######

def main_menu():
    """Main menu of the Work Log program."""
    choice = None
    clear_screen()

    while True:
        print("WORK LOG")
        for key, value in main_menu_options.items():
            print("{}) {}".format(key, value.__doc__))
        print("c) Quit program")
        choice = input("> ").lower().strip()

        if choice in main_menu_options:
            main_menu_options[choice]()
        elif choice == 'c':
            clear_screen()
            print("Thank you for using the Work Log program!\n")
            break
        else:
            clear_screen()
            print("That is not a valid menu option.")


def search_menu():
    """Search in existing entries"""
    clear_screen()
    while True:
        if Log.select().count() == 0:
            clear_screen()
            return_to_menu = input("There are no logs in the system. " +
                                   "Press 'Enter' to return to the " +
                                   "main menu.")
            clear_screen()
            break
        print("Do you want to search by:\n"
              "a) Exact Date\n"
              "b) Date Range\n"
              "c) Time Spent\n"
              "d) Search Term\n"
              "e) Username List\n"
              "f) Enter Username\n\n"
              "[M]ain Menu\n"
              )
        search_selection = input("> ").lower().strip()
        if search_selection == 'a':
            search_date()
        elif search_selection == 'b':
            search_range()
        elif search_selection == 'c':
            search_time()
        elif search_selection == 'd':
            search_term()
        elif search_selection == 'e':
            search_list()
        elif search_selection == 'f':
            search_username()
        elif search_selection == 'm':
            clear_screen()
            break
        else:
            clear_screen()
            print("That is not a valid selection. "
                  "Please choose an option from the menu.\n"
                  )
            continue

###################################
#Log Creation and Search Functions#
###################################

def add_log():
    """Add new entry"""
    clear_screen()
    task_date = get_date("What is the date of the task? (MM/DD/YYYY): ")
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


def view_log(logs):
    """Display selected logs."""
    clear_screen()
    index = 0
    counter = 1
    while True:
        print("Date: {}\n".format(datetime.datetime.strftime(logs[index].task_date, '%m/%d/%Y')) +
              "Title: {}\n".format(logs[index].task_title) +
              "Time Spent: {}\n".format(logs[index].task_time) +
              "Notes: {}\n\n".format(logs[index].task_notes) +
              "Result {} of {}".format(counter, logs.select().count())
              )
        if logs.select().count() == 1:
            nav_options = 'des'
        elif counter <= 1:
            nav_options = 'neds'
        elif counter > 1 and counter < logs.select().count():
            nav_options = 'pneds'
        elif counter == logs.select().count():
            nav_options = 'peds'
        nav_bar(nav_options)
        menu_option = input("> ").lower().strip()
        if menu_option not in nav_options or menu_option == '':
            clear_screen()
            print("Sorry, that is not a valid selection.\n")
        elif menu_option == 'n':
            clear_screen()
            counter += 1
            index += 1
        elif menu_option == 'p':
            clear_screen()
            counter -= 1
            index -= 1
        elif menu_option == 'd':
            logs[index].delete_instance()
            index = 0
            counter = 1
            clear_screen()
            next = input("The log has been deleted. " +
                         "Press 'Enter' to continue.")
            clear_screen()
            if logs.select().count() == 0:
                index = 0
                counter = 1
                clear_screen()
                break
        elif menu_option == 'e':
            edit_log(logs[index])
            index = 0
            counter = 1
            clear_screen()
            next = input("The log has been edited. " +
                         "Press 'Enter' to continue.")
            clear_screen()
            break
        elif menu_option == 's':
            clear_screen()
            break


def search_date():
    """Search logs using an exact date."""
    date_list = []
    logs = Log.select().order_by(Log.task_date.desc())
    for log in logs:
        if log.task_date not in date_list:
            date_list.append(log.task_date)
    clear_screen()
    while True:
        try:
            print("For which date would you like to see the work logs?\n")
            counter = 1
            for date in date_list:
                print("  " + str(counter) + ") " +
                      datetime.datetime.strftime(date, '%m/%d/%Y'))
                counter += 1
            date_selection = int(input("\n> ")) - 1
        except ValueError:
                clear_screen()
                print("Sorry, that is not a valid selection.")
                continue
        if date_selection not in range(0, (len(date_list))):
            clear_screen()
            print("Sorry, that is not a valid selection.")
            continue
        else:
            view_log(Log.select().where(Log.task_date==
                                        date_list[date_selection]))
            break


def search_range():
    """Search logs by providing a date range."""
    clear_screen()
    print("What beggining date would you like to use for the range? " +
          "(MM/DD/YYYY)\n")
    begin_range = get_date("> ")
    clear_screen()
    while True:
        print("What ending date would you like to use for the range? " +
              "(MM/DD/YYYY)\n")
        end_range = get_date("> ")
        if begin_range > end_range:
            clear_screen()
            print("The ending date must be after " +
                  "{}.".format(datetime.datetime.strftime(begin_range, '%m/%d/%Y')))
        else:
            break
    logs = Log.select().where((Log.task_date >= begin_range) &
                                    (Log.task_date <= end_range))
    if logs.select().count() == 0:
        clear_screen()
        return_to_menu = input("There are no logs in that date range.\n" +
                               "You will be returned to the search menu.\n" +
                               "Press 'Enter' to continue.")
        clear_screen()
    else:
        view_log(logs)


def search_time():
    """Search logs by time spent."""
    clear_screen()
    while True:
        try:
            print("Search the logs by the amount of time spent on the "
                  "task.\nEnter the number of minutes.")
            time_spent = int(input("> "))
            break
        except ValueError:
            clear_screen()
            print("The time must be entered using numerical digits.")
            continue
    logs = Log.select().where(Log.task_time == time_spent)
    if logs.select().count() == 0:
        clear_screen()
        return_to_menu = input("There are no logs lasting that amount of time.\n" +
                               "You will be returned to the search menu.\n" +
                               "Press 'Enter' to continue.")
        clear_screen()
    else:
        view_log(logs)


def search_term():
    """Search logs by search term."""
    clear_screen()
    print("Search logs by entering a search term.")
    term = input("> ")
    logs = Log.select().where((Log.task_title.contains(term)) |
                              (Log.task_notes.contains(term)))
    if logs.select().count() == 0:
        clear_screen()
        return_to_menu = input("There are no logs matching that term.\n" +
                               "You will be returned to the search menu.\n" +
                               "Press 'Enter' to continue.")
        clear_screen()
    else:
        view_log(logs)


def search_list():
    """Search using a list of usernames."""
    username_list = []
    logs = Log.select().order_by(Log.username)
    for username in logs:
        if username.username not in username_list:
            username_list.append(username.username)
    clear_screen()
    while True:
        try:
            print("For which username would you like to see the work logs?\n")
            counter = 1
            for username in username_list:
                print("  " + str(counter) + ") " + username)
                counter += 1
            username_selection = int(input("\n> ")) - 1
        except ValueError:
                clear_screen()
                print("Sorry, that is not a valid selection.")
                continue
        if username_selection not in range(0, (len(username_list))):
            clear_screen()
            print("Sorry, that is not a valid selection.")
            continue
        else:
            view_log(Log.select().where(Log.username ==
                                        username_list[username_selection]))
            break


def search_username():
    """Search logs by a username supplied by the user."""
    username_list = []
    clear_screen()
    print("What user's logs would you like to view?")
    username = input("> ")
    logs = Log.select().where(Log.username.contains(username)).order_by(Log.username)
    for username in logs:
        if username.username not in username_list:
            username_list.append(username.username)
    if len(username_list) == 0:
        clear_screen()
        return_to_menu = input("There are no logs from that user.\n" +
                               "You will be returned to the search menu.\n" +
                               "Press 'Enter' to continue.")
        clear_screen()
    elif len(username_list) == 1:
        logs = Log.select().where(Log.username.contains(username_list[0]))
        view_log(logs)
    elif len(username_list) > 1:
        clear_screen()
        while True:
            try:
                print("For which username would you " +
                      "like to see the work logs?\n")
                counter = 1
                for username in username_list:
                    print("  " + str(counter) + ") " + username)
                    counter += 1
                username_selection = int(input("\n> ")) - 1
            except ValueError:
                    clear_screen()
                    print("Sorry, that is not a valid selection.")
                    continue
            if username_selection not in range(0, (len(username_list))):
                clear_screen()
                print("Sorry, that is not a valid selection.")
                continue
            else:
                view_log(Log.select().where(Log.username ==
                                            username_list[username_selection]))
                break


main_menu_options = OrderedDict([
    ('a', add_log),
    ('b', search_menu),
])

if __name__ == '__main__':
    initialize()
    username = login()
    main_menu()
