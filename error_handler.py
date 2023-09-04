import sys
import pickle
from tkinter import messagebox


def io_error_handler(func):
    # Pickle error handler decorator
    def inner1(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except IOError:
            messagebox.showerror(
                "Error", "Could not open the file, check the file's permissions")
        except pickle.PickleError:
            messagebox.showerror("Error", "Could not pickle the {} object.")
        sys.exit(1)

    return inner1
