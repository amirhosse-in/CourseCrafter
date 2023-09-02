import requests
from bs4 import BeautifulSoup
import re
import json
from models import *


def get_department_and_courses():
    departments = []
    courses = []

    url = "https://edu.sharif.edu/list/courses"

    # Fetch the page content
    response = requests.get(url)
    page_content = response.content

    # Create a BeautifulSoup object
    soup = BeautifulSoup(page_content, "html.parser")

    # Find the <select> element
    select_element = soup.find("select", id="departmentID")

    # Find all <option> elements within the <select>
    options = select_element.find_all("option")
    for option in options[1:]:
        value = int(option["value"])
        text = option.get_text(strip=True)
        department = Department(value, text)
        departments.append(department)

    updated_page_content = str(soup)
    # Extract the JavaScript variable 'courses' from the updated_page_content
    matches = re.search(
        r'var courses = (\[.*?\]);', updated_page_content, re.DOTALL)
    if matches:
        courses_js = matches.group(1)
        courses_list = json.loads(courses_js)
        for course in courses_list:
            id = int(course[0])
            group = int(course[1])
            credit = int(course[2])
            title = course[3]
            instructor = course[4]
            time = course[5]
            details = course[6]
            link = course[7]
            postgraduate = int(course[8]) != 0
            _course = Course(id, group, credit, title, instructor,
                             time, details, link, postgraduate)
            courses.append(_course)
    else:
        raise LookupError("No 'courses' variable found in the content.")

    Department.save_to_file(departments, "departments.cc")
    Course.save_to_file(courses, "courses.cc")
    return departments, courses
