import sys
import pickle
from tkinter import messagebox


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
