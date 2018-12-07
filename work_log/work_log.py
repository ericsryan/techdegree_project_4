from login import login
from login import register
from model import initialize
from screens import login_screen
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
            return False
        else:
            login(login_input)


def main_menu():
    pass

if __name__ == '__main__':
    initialize()
    login_menu()
