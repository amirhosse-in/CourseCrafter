import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models import *
import edu


class CourseBox:
    def __init__(self, root, course, array):
        self.root = root
        self.course = course
        self.array = array

        self.background = "orange"
        self.create_frame()

    def create_frame(self):
        self.frame = tk.Frame(self.root, width=100, height=50, bg=self.background)
        self.frame.place(x=500, y=50)
        self.add_course_name()
        self.add_course_instructor()
        #self.add_delete_button()

    def delete_box(self):
        self.frame.destroy()  # Remove the frame from the GUI
        self.array.remove(self)  # Remove the instance from the array

    def add_delete_button(self):
        delete_button = tk.Button(self.frame, text="X", command=self.delete_box)
        delete_button.pack(side="bottom")

    def add_course_name(self):
        name_label = tk.Label(self.frame, text=self.course.name, font=("TkDefaultFont", 11), bg=self.background)
        name_label.pack(side="top")
    def add_course_instructor(self):
        instructor_label = tk.Label(self.frame, text=self.course.instructor, font=("TkDefaultFont", 11), bg=self.background)
        instructor_label.pack(side="top")


class ScheduleForm:
    def __init__(self, root, departments, courses):
        self.root = root
        self.root.title("Course Crafter")

        self.departments = departments
        self.courses = courses
        self.showing_postgraduate = False

        self.listbox_courses = []
        self.grid_courses = []
        self.selected_department = None
        self.selected_course = None

        self.canvas = tk.Canvas(self.root, width=1300, height=800)
        self.canvas.pack()

        self.create_left_frame()
    
    def create_right_frame(self):
        self.days = ['پنجشنبه', 'چهار شنبه', 'سه شنبه', 'دوشنبه', 'یکشنبه', 'شنبه']
        self.hours = list(range(7, 21))

    def create_days(self, root):
        days_frame = tk.Frame(root, bg = "orange")
        
        #TODO

        days_frame.pack(side="top")


    def create_left_frame(self):
        self.left_frame = tk.Frame(self.root, height=750, width=300)
        self.left_frame.place(x=10, y=15)
        
        self.create_left_first_row(self.left_frame)
        self.create_search_box(self.left_frame)
        self.create_listbox(self.left_frame)
        self.create_course_info(self.left_frame)
        self.create_add_button(self.left_frame)

    def create_left_first_row(self, root):
        self.left_first_row = tk.Frame(root)
        
        self.create_checkbox(self.left_first_row)
        self.create_combo(self.left_first_row)

        self.left_first_row.pack(side="top")

    
    def create_checkbox(self, root):
        self.checkbox_var = tk.BooleanVar()
        self.checkbox_var.set(False)

        self.checkbox = tk.Checkbutton(root, text="تحصیلات تکمیلی", variable=self.checkbox_var, command=lambda: self.update_department())
        self.checkbox.pack(side="left")

    def create_combo(self, root):
        names = ["دانشکده را انتخاب کنید"]
        ids = []

        for department in self.departments:
            names.append(department.name)
            ids.append(department.id)

        self.selected_item = tk.StringVar(value=names[0])
        self.combo = ttk.Combobox(root, values=names, textvariable=self.selected_item, justify="right", width=17)
        self.combo.pack(side="right")
        self.combo.bind("<<ComboboxSelected>>", self.update_department)

    def update_department(self, event=None):
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
            if course.id // 1000 == self.selected_department.id and self.checkbox_var.get() == course.postgraduate:
                self.listbox_courses.append(course)

        self.update_listbox()

    def create_search_box(self, root):
        self.search_entry = tk.Entry(root, width=29, justify="right")
        self.search_entry.pack(side="top", anchor="w")
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
            if check and self.checkbox_var.get() == course.postgraduate:
                secondary_listbox_courses.append(course)

        self.listbox_courses = secondary_listbox_courses
        self.update_listbox()

    def create_listbox(self, root):
        # Create a Listbox widget
        list_frame = tk.Frame(root)

        self.listbox = tk.Listbox(list_frame, selectmode=tk.NONE, font=("Helvetica", 15), justify="right",height=25)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.listbox.pack(side="left", fill="both", padx=0, pady=0)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.config(command=self.listbox.yview, troughcolor="black")
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right",fill="both", padx=0)

        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        list_frame.pack(side="top", fill="x", pady = 5)

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            self.selected_course = self.listbox_courses[index]
            course_info = f"کد درس: {self.selected_course.id}\n" \
                f"نام درس: {self.selected_course.name}\n" \
                f"گروه: {self.selected_course.group}\n" \
                f"واحد: {self.selected_course.credit}\n" \
                f"مدرس: {self.selected_course.instructor}\n" \
                f"زمان کلاس: {self.selected_course.time}\n" \
                f"توضیحات: {self.selected_course.details}\n" \
                f"کلاس مجازی:\n{self.selected_course.virtual_class}" 

            self.details_label.config(text=course_info)

    def create_course_info(self, root):
        self.course_info_frame = tk.Frame(root, height=230, width=290)
        self.course_info_frame.pack(side="top")
        self.details_label = tk.Label(
            self.course_info_frame, text="اطلاعات درس", anchor="e", justify="right", wraplength=270)
        self.details_label.place(x=0, y=0, width=290)

    def create_add_button(self, root):
        self.add_course_button = tk.Button(root, text="اضافه کردن درس", command=self.add_course)
        self.add_course_button.pack(side="top", fill="y")

    def add_course(self):
        if self.selected_course == None or self.selected_course.time == "":
            messagebox.showerror("Error", "The course does not have a specified time, if you think that the time is specified, delete the .cc files and run the program again.", icon="error")
        else:
            #self.grid_courses
            course_box = CourseBox(self.root, self.selected_course, self.grid_courses)

    def update_listbox(self):
        # Insert items into the Listbox
        for course in self.listbox_courses:
            self.listbox.insert(tk.END, course.name)


if __name__ == "__main__":

    try:
        # Reading saved information
        departments = Department.read_from_file("departments.cc")
        courses = Course.read_from_file("courses.cc")
    except:
        # Getting information from edu list
        departments, courses = edu.get_department_and_courses()
        edu.Course.save_to_file(courses, "courses.cc")
        edu.Department.save_to_file(departments, "departments.cc")

    root = tk.Tk()
    app = ScheduleForm(root, departments, courses)
    root.mainloop()
