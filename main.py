import tkinter as tk
from tkinter import ttk
from models import *
import edu

class ScheduleForm:
    def __init__(self, root, departments, courses):
        self.root = root
        self.root.title("Schedule Form")
        
        self.departments = departments
        self.courses = courses

        self.listbox_courses = []
        self.selected_department = None
        self.days = ['پنجشنبه', 'چهار شنبه', 'سه شنبه', 'دوشنبه', 'یکشنبه', 'شنبه']
        self.hours = list(range(7, 21))


        self.create_schedule_grid()
        self.create_combo()
        self.create_search_box()
        self.create_list_interface()

        
    def create_schedule_grid(self):
        canvas = tk.Canvas(self.root, width=1010, height=900)
        canvas.pack()
        
        cell_width = 100
        cell_height = 50
        horizental_padding = 3 * cell_width + 5
        vertical_padding = 15
        
        for day_index, day in enumerate(self.days):
            canvas.create_text(horizental_padding + cell_width * (day_index + 0.5),vertical_padding + cell_height / 2, text=day)
            
        for hour_index, hour in enumerate(self.hours):
            canvas.create_text(horizental_padding + cell_width * len(self.days) + cell_width / 2,vertical_padding + cell_height + cell_height * (hour_index + 0.5), text=f"{hour}:00")
            
        for day_index in range(len(self.days)+1):
            for hour_index in range(len(self.hours)+1):
                x0 = day_index * cell_width + horizental_padding 
                y0 = hour_index * cell_height + vertical_padding
                x1 = x0 + cell_width
                y1 = y0 + cell_height
                canvas.create_rectangle(x0, y0, x1, y1, outline="lightgrey")
    
    def create_combo(self):
        names = ["دانشکده را انتخاب کنید"]
        ids = []

        for department in self.departments:
            names.append(department.name)
            ids.append(department.id)
        
        self.selected_item = tk.StringVar(value=names[0])
        self.combo = ttk.Combobox(self.root, values=names, textvariable=self.selected_item, justify="right", width=30)
        self.combo.place(x = 5, y = 15)
        self.combo.bind("<<ComboboxSelected>>", self.update_department)


    def update_department(self, event = None):
        # Clear Listbox
        self.listbox.delete(0, tk.END)
        self.listbox_courses.clear()

        selected_index = self.combo.current()
        if selected_index > 0:  # Avoid the placeholder "دانشکده را انتخاب کنید"
            self.selected_department = self.departments[selected_index - 1]
        else:
            self.selected_department = None
            return
        
        for course in courses:
            if course.id // 1000 == self.selected_department.id:
                self.listbox_courses.append(course)
        
        self.update_listbox()
        

    def create_search_box(self):
        self.search_entry = tk.Entry(self.root, width=29)
        self.search_entry.place(x = 8, y = 45)
        self.search_entry.bind("<KeyRelease>", self.search)

    def search(self, event):
        self.update_department()

        # Clear listboxs
        self.listbox.delete(0, tk.END)
        
        secondary_listbox_courses = []

        search_text = self.search_entry.get().lower().split(' ')
        

        for course in self.listbox_courses:
            course_string = course.get_searchable_string()
            check = True
            for word in search_text:
                if word not in course_string:
                    check = False
                    break
            if check:
                secondary_listbox_courses.append(course)
        
        self.listbox_courses = secondary_listbox_courses
        self.update_listbox()

    def create_list_interface(self):
        # Create a Listbox widget
        self.listbox = tk.Listbox(self.root, selectmode=tk.NONE, font=("Helvetica", 15), width=30, height=25, justify="right")
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.listbox.place(x = 10, y = 75)
        
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.place(x = 285,y = 75, height=450)
        scrollbar.config(command = self.listbox.yview, troughcolor="black")
        self.listbox.config(yscrollcommand = scrollbar.set)

        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.details_label = tk.Label(self.root, text="Course Details:")
        self.details_label.pack(pady=10)

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            selected_course = self.listbox_courses[index]
            self.details_label.config(text=f"Group ID: {selected_course.group}\n"
                                           f"Course ID: {selected_course.id}\n"
                                           f"Course Name: {selected_course.name}\n"
                                           f"Department: {selected_course.id//1000}")
    
    def update_listbox(self):
        # Insert items into the Listbox
        for course in self.listbox_courses:
            self.listbox.insert(tk.END, course.name)
        
                
if __name__ == "__main__":
    
    # Getting information from edu list
    # departments, courses = edu.get_department_and_courses()

    departments = Department.read_from_file("departments.cc")
    courses = Course.read_from_file("courses.cc")

    root = tk.Tk()
    app = ScheduleForm(root, departments, courses)
    root.mainloop()
