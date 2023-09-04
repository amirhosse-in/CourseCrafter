import sys
import pickle
from tkinter import messagebox
import requests


def io_error_handler(func):
    # Pickle error handler decorator
    def inner1(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            raise FileNotFoundError()  # Handled in the code logic
        except PermissionError:
            messagebox.showerror(
                "Error", "Could not open the file, check the file's permissions")
        except pickle.PickleError:
            messagebox.showerror(
                "Error", "Could not read the save file, is it corrupted?")
        sys.exit(1)

    return inner1


def connection_error_handler(func):
    # Connection error handler decorator
    def inner1(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "Connection Error", "There was a problem with your connection, please check internet connectivity and try again")

    return inner1
