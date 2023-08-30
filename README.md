# CourseCrafter

CourseCrafter is a Python project modeled after the *term.inator* project. It's designed to simplify the process of pre-choosing courses for a semester. The project provides a user-friendly interface to select courses based on your preferences and schedule.

## Overview

CourseCrafter automates the process of updating course information, so you don't need to worry about keeping the database up to date. The application automatically requests the latest course information from `edu.sharif.edu/list/courses` and updates itself accordingly. If you wish to update the courses list, you have to remove the `.cc` files located next to the `.py` files.

## Requirements

Before running the CourseCrafter project, ensure you have the following installed:

- ### Python 3.11
- `tkinter` library
- `pickle` library
- `re` library
- `bs4` (Beautiful Soup) library
- `json` library
- `requests` library

## Running the Project

To run the CourseCrafter project, follow these steps:

1. Ensure you have met the requirements listed above.
2. Download or clone the CourseCrafter repository to your local machine.
3. Open a terminal or command prompt and navigate to the project's directory.
4. Run the main Python file by executing `python main.py`.

## Contributing

If you're interested in contributing to CourseCrafter, feel free to fork the project, make improvements, and submit pull requests. Your contributions are greatly appreciated and can help make the project even better.

**Note:** This project was inspired by *term.inator* and aims to provide a similar but simplified experience for pre-choosing courses. It's not affiliated with or endorsed by *term.inator* or any educational institution.
