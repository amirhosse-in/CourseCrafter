import requests
from bs4 import BeautifulSoup
import re
import json
from models import *
from error_handler import connection_error_handler


@connection_error_handler
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
            postgraduate = False #TODO CHECK HERE #int(course[8]) != 0
            _course = Course(id, group, credit, title, instructor,
                             time, details, link, postgraduate)
            courses.append(_course)
    else:
        raise LookupError("No 'courses' variable found in the content.")

    return departments, courses


def login(username, password):
    session = requests.session()
    response = session.post("https://edu.sharif.edu/login.do", data={
        "username": username,
        "password": password,
        "command": "login",
    })
    if session.cookies.get("JSESSIONID"):
        session.post("https://edu.sharif.edu/action.do", data={
            "changeMenu": "OnlineRegistration",
            "isShowMenu": "",
            "id": "",
            "commandMessage": "",
            "defaultCss": "",
        })
        session.post("https://edu.sharif.edu/register.do", data={
            "changeMenu": "OnlineRegistration*OfficalLessonListShow",
            "isShowMenu": "",
        })
        return session
    return None


def get_finals_from_department(session, department_id):
    response = session.post("https://edu.sharif.edu/register.do", data={
        "level": "0",
        "teacher_name": "",
        "sort_item": "1",
        "depID": str(department_id)
    })
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, "html.parser")
    courses = {}
    tables = soup.find_all("table", {"class": "contentTable"})
    for table in tables:
        rows = table.find_all("tr")
        rows = rows[2:]
        for row in rows:
            cols = row.find_all("td")
            try:
                course_id = int(cols[0].get_text(strip=True))
                course_group = int(cols[1].get_text(strip=True))
                course_units = int(cols[2].get_text(strip=True))
            except:
                continue
            final_time = cols[8].get_text(strip=True)
            course_key = f'{course_id}-{course_group}-{course_units}'
            courses[course_key] = final_time
    return courses
