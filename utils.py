"""Utilities for the Work Log program."""

import datetime
import os
import string


def clear_screen():
    """Clear the screen for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')


def convert_to_datetime(date):
    """Return datetime object from date string."""
    return datetime.datetime.strptime(date, '%m/%d/%Y')


def format_date(date):
    """Replace date seperators with forward slashes for consistancy."""
    formatted_date = ''
    for character in date:
        if character not in string.digits and character != '/':
            formatted_date += '/'
        else:
            formatted_date += character
    return formatted_date


def get_date(question):
    """Accept date from user then validate and return datetime object."""
    while True:
        try:
            date_input = input(question)
            formatted_date = format_date(date_input)
            converted_date = convert_to_datetime(formatted_date)
        except ValueError:
            clear_screen()
            print("The date was not formatted correctly. Please try again.")
            continue
        else:
            break
    return converted_date


def validate_minutes(question):
    """Validate and return number of minutes."""
    while True:
        try:
            minutes = int(input(question))
        except ValueError:
            clear_screen()
            print("Sorry, you must enter the number of minutes as an integer.")
            continue
        else:
            break
    return minutes
