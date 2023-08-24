import pickle

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
    def __init__(self, id, group, credit, name, instructor, time, details, virtual_class, final = None):
        self.id = id
        self.group = group 
        self.credit = credit 
        self.name = name 
        self.instructor = instructor 
        self.time = time 
        self.details = details 
        self.virtual_class = virtual_class 
        self.final = final
    
    @staticmethod
    def save_to_file(array, address):
        with open(address, "wb") as file:
            pickle.dump(array, file)

    @staticmethod
    def read_from_file(address):
        with open(address, "rb") as file:
            return pickle.load(file)
    
    def get_searchable_string(self):
        return f"{self.id} {self.name} {self.instructor} {self.details}"

