"""Utilities for the Work Log program."""

import os


def clear_screen():
    """Clear the screen for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')
