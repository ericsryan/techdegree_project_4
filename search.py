from collections import OrderedDict
from utils import clear_screen

def search_menu():
    """Search in existing entries"""
    choice = None

    while choice != 'm':
        clear_screen()
        print("Do you want to search by:")
        for key, value in search_menu_actions.items():
            print("{}) {}".format(key, value.__doc__))
        print("\n[M]ain Menu")
        choice = input("\n> ").lower().strip()

        if choice in search_menu_actions:
            clear_screen()
            search_menu_actions[choice]()


def search_date():
    """Exact date"""
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
    """Range of dates"""
    pass


def search_time():
    """Time spent"""
    pass


def search_term():
    """Search by term"""
    pass


def search_username_list():
    """Username list"""
    pass


def search_username_term():
    """Lookup username"""
    pass


search_menu_actions = OrderedDict([
    ('a', search_date),
    ('b', search_range),
    ('c', search_time),
    ('d', search_term),
    ('e', search_username_list),
    ('f', search_username_term)
])
