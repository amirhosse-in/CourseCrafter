import pickle
import re

class Department:
    def __init__(self, department_id, department_name):
        self.id = department_id
        self.name = department_name

    @staticmethod
    def save_to_file(array, address):
        with open(address, "wb") as file:
            pickle.dump(array, file)

    @staticmethod
    def read_from_file(address):
        with open(address, "rb") as file:
            return pickle.load(file)

class Course:
    def __init__(self, id, group, credit, name, instructor, time, details, virtual_class, postgraduate, final = None):
        self.id = id
        self.group = group 
        self.credit = credit 
        self.name = name 
        self.instructor = instructor 
        self.time = time 
        self.details = details 
        self.virtual_class = virtual_class 
        self.final = final
        self.postgraduate = postgraduate
        try:
            self.days, self.start, self.end = Course.get_day_and_hour(time)
        except:
            print(f"There is no time for Course {id}:{name}")
            
        
    
    @staticmethod
    def save_to_file(array, address):
        with open(address, "wb") as file:
            pickle.dump(array, file)

    @staticmethod
    def read_from_file(address):
        with open(address, "rb") as file:
            return pickle.load(file)
    
    @staticmethod
    def get_day_and_hour(s):
        pattern = r'([^0-9]+)\s+(\d{1,2}:\d{2}|\d{1,2})\s+تا\s+(\d{1,2}:\d{2}|\d{1,2})'
        match = re.search(pattern, s)

        # result is [[first_day, second_day], [starting_hour, starting_minutes], [ending_hour, ending_minutes]]
        result = []
        if match:
            days = match.group(1)
            start = match.group(2)
            end = match.group(3)
            
            separated_days = days.split(' و ')
            first_day = Course.get_day_from_str(separated_days[0])
            second_day = None
            if len(separated_days) > 1:
                second_day = Course.get_day_from_str(separated_days[1])
            result.append([first_day, second_day])
            result.append(Course.get_hour_from_str(start))
            result.append(Course.get_hour_from_str(end))
            return result
        return -1
            
    @staticmethod
    def get_day_from_str(day_in_str):
        days_of_week = {
            "شنبه":0,
            "یک":1,
            "دو":2,
            "سه":3,
            "چهار":4,
            "پنج":5
        }

        for key,value in days_of_week.items():
            if str(day_in_str).startswith(key):
                return value
        
        return -1
    
    @staticmethod
    def get_hour_from_str(hour_in_str):
        if ':' in hour_in_str:
            separated = hour_in_str.split(':')
            return [int(separated[0]), int(separated[1])]
        else:
            return [int(hour_in_str), 0]

    @staticmethod
    def check_conflict(course1, course2):
        if course1.end <= course2.start or course1.start >= course2.end:
            return False
        if course1.days[0] == course2.days[0]:
            return True
        if course1.days[1] != None and course1.days[1] == course2.days[0]:
            return True
        if course2.days[1] != None and course2.days[1] == course1.days[0]:
            return True
        return False
    def get_searchable_string(self):
        return f"{self.id} {self.name} {self.instructor} {self.details}"

