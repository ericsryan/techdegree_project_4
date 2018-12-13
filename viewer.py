import datetime

from utils import clear_screen
from utils import convert_to_datetime


# Take in logs
# Print the first log
# Give options to move to the next or previous log if available
# Give option to edit or delete the present log
# Give option to return to the search menu

index = 0
counter = 1
logs = []


def view_logs(logs):
    """Logic to dispay work logs."""
    clear_screen()
    while True:
        if logs.select().count() == 0:
            __ = input("There are no logs matching the search criteria. " +
                       " Press 'Enter' to return to the search menu. ")
            break
        else:
            print(draw_log())
            if logs.select().count() == 1:
                menu_bar('eds')
            elif counter == 1:
                menu_bar('neds')
            elif (counter > 1 and counter <
                      logs.select().count()):
                menu_bar('pneds')
            elif counter == logs.select().count():
                menu_bar('peds')


class Viewer:
    def __init__(self, logs):
        self.logs = logs
        self.index = 0
        self.counter = 1

    def view_logs(self):
        """Logic to dispay work logs."""
        clear_screen()
        self.keep_going = True
        while self.keep_going:
            if self.logs.select().count() == 0:
                __ = input("There are no logs matching the search criteria. " +
                           " Press 'Enter' to return to the search menu. ")
                break
            else:
                print(self.draw_log())
                if self.logs.select().count() == 1:
                    self.menu_bar('eds')
                elif self.counter == 1:
                    self.menu_bar('neds')
                elif (self.counter > 1 and self.counter <
                          self.logs.select().count()):
                    self.menu_bar('pneds')
                elif self.counter == self.logs.select().count():
                    self.menu_bar('peds')

    def draw_log(self):
        return ("Date: {}\n".format(datetime.datetime.strftime(
                                    self.logs[self.index].task_date,
                                    '%m/%d/%Y')) +
                "Title: {}\n".format(self.logs[self.index].task_title) +
                "Time Spent: {}\n".format(self.logs[self.index].task_time) +
                "Notes: {}\n\n".format(self.logs[self.index].task_notes) +
                "Result {} of {}".format(self.counter,
                                         self.logs.select().count())
                )

    def menu_bar(self, options):
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
            self.keep_going = False

    def edit_log(self):
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
                      datetime.datetime.strftime(self.logs[self.index].task_date, '%m/%d/%Y') +
                      "\n\nWhat would you like the date to be?\n")
                new_date = convert_to_datetime("> ")
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

    def delete_log(self):
        """Delete a log from the database."""
        if input("Are you sure you want to delete " +
                 "the log? Y/N: ").lower() == 'y':
            self.logs[self.index].delete_instance()
            if self.index >= 1:
                self.index -= 1
            if self.counter >= 2:
                self.counter -= 1
            __ = input("The log has been deleted. Press 'Enter' to continue.")
            clear_screen()
