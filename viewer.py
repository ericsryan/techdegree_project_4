"""Viewer functions allow logs to be displayedself.

The viewer provides the functions to allow the user to view the logs that have
been selected. The user can page through the logs and choose to edit or
delete the log that is being viewed.
"""
import datetime

from models import Log
from utils import clear_screen
from utils import get_date
from utils import validate_minutes


class Viewer(object):
    """View selected work logs."""

    def __init__(self, logs):
        """Store work logs and set index and counter."""
        self.logs = logs
        self.index = 0
        self.counter = 1

    def view_logs(self):
        """Logic to dispay work logs."""
        clear_screen()
        self.keep_going = True
        while self.keep_going:
            if len(self.logs) == 0:
                __ = input("There are no logs matching the search criteria. " +
                           " Press 'Enter' to return to the search menu. ")
                clear_screen()
                return False
                break
            else:
                print(self.draw_log())
                if len(self.logs) == 1:
                    self.menu_bar('eds')
                    return True
                elif self.counter == 1:
                    self.menu_bar('neds')
                    return True
                elif (self.counter > 1 and self.counter <
                      len(self.logs)):
                    self.menu_bar('pneds')
                    return True
                elif self.counter == len(self.logs):
                    self.menu_bar('peds')
                    return True

    def draw_log(self):
        """Format and draw the work log."""
        return ("Logged by: {}\n\n".format(self.logs[self.index].username) +
                "Date: {}\n".format(datetime.datetime.strftime(
                                    self.logs[self.index].task_date,
                                    '%m/%d/%Y')) +
                "Title: {}\n".format(self.logs[self.index].task_title) +
                "Time Spent: {}\n".format(self.logs[self.index].task_time) +
                "Notes: {}\n\n".format(self.logs[self.index].task_notes) +
                "Result {} of {}".format(self.counter,
                                         len(self.logs))
                )

    def menu_bar(self, options):
        """Create a menu bar for the log viewer."""
        menu_bar_options = [
            ('p', '[P]revious'),
            ('n', '[N]ext'),
            ('e', '[E]dit'),
            ('d', '[D]elete'),
            ('s', '[S]earch Menu')
        ]
        nav_bar = []
        for option in menu_bar_options:
            if option[0] in options:
                nav_bar.append(option[1])
                nav_bar.append(' | ')
        del nav_bar[-1]
        print(''.join(nav_bar))
        menu_selection = input("> ").lower().strip()
        if menu_selection not in options:
            clear_screen()
            print("That is not a valid selection.")
        elif menu_selection == 'p':
            self.index -= 1
            self.counter -= 1
            clear_screen()
        elif menu_selection == 'n':
            self.index += 1
            self.counter += 1
            clear_screen()
        elif menu_selection == 'e':
            self.edit_log()
        elif menu_selection == 'd':
            self.delete_log()
        elif menu_selection == 's':
            clear_screen()
            self.keep_going = False

    def edit_log(self):
        """Edit the selected work log."""
        clear_screen()
        while True:
            print("Which field would you like to edit?\n\n" +
                  "  a) Date\n" +
                  "  b) Title\n" +
                  "  c) Time\n" +
                  "  d) Notes\n")
            selection = input("> ").lower().strip()
            if selection not in 'abcd':
                clear_screen()
                print("That is not a valid selection.")
                return False
                continue
            elif selection == 'a':
                clear_screen()
                print("Original Date: " +
                      datetime.datetime.strftime(
                          self.logs[self.index].task_date, '%m/%d/%Y') +
                      "\n\nWhat would you like the date to be?\n")
                new_date = get_date("> ")
                self.logs[self.index].update(task_date=new_date).where(
                    Log.id == self.logs[self.index]).execute()
            elif selection == 'b':
                clear_screen()
                print("Original Title: " + self.logs[self.index].task_title +
                      "\n\nWhat would you like the title to be?\n")
                new_title = input("> ")
                self.logs[self.index].update(task_title=new_title).where(
                    Log.id == self.logs[self.index]).execute()
            elif selection == 'c':
                clear_screen()
                print("Original Time: " + str(
                          self.logs[self.index].task_time) +
                      "\n\nWhat would you like the time to be?\n")
                new_time = validate_minutes("> ")
                self.logs[self.index].update(task_time=new_time).where(
                    Log.id == self.logs[self.index]).execute()
            elif selection == 'd':
                clear_screen()
                print("Original Notes: " + self.logs[self.index].task_notes +
                      "\n\nWhat would you like the notes to be?\n")
                new_notes = input("> ")
                self.logs[self.index].update(task_notes=new_notes).where(
                    Log.id == self.logs[self.index]).execute()
            clear_screen()
            __ = input("The log has been edited. Press 'Enter' to continue. ")
            clear_screen()
            self.keep_going = False
            break

    def delete_log(self):
        """Delete a log from the database."""
        if input("Are you sure you want to delete " +
                 "the log? Y/N: ").lower() == 'y':
            self.logs[self.index].delete_instance()
            clear_screen()
            __ = input("The log has been deleted. Press 'Enter' to continue.")
            clear_screen()
            self.keep_going = False
        else:
            clear_screen()
