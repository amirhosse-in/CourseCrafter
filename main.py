import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import atexit
from models import *
from bidi.algorithm import get_display
import edu
import arabic_reshaper
import threading


class CourseBox:
    def __init__(self, root, course, selected_courses, form, layer=0, is_hovered=False):
        self.root = root
        self.course = course
        self.selected_courses = selected_courses
        self.form = form
        self.layer = layer
        if not is_hovered:
            self.background = ["#C08261", "#C0A261", "#C0C061", "#AEC061", "#61C0A2",
                               "#61C0C0", "#61AEC0", "#6161C0", "#A261C0", "#C061C0", "#C061A2"][layer % 11]
        else:
            self.background = "#a6c8ff"

        self.default_block_width = 150
        self.default_block_height = 50
        self.frame1, self.frame2 = self.create_frame(0), self.create_frame(1)

        if not is_hovered:
            self.form.total_credits += course.credit
            self.form.root.title(
                f"Course Crafter - {self.form.total_credits} Credits selected")

    def __repr__(self):
        return f'{self.course} {self.layer}'

    def create_frame(self, day):
        if self.course.days[day] == None:
            return None
        x, y, height = self.calculate_position(day)
        frame = tk.Frame(self.root, width=self.default_block_width - 2 -
                         self.layer * 5, height=height - 1 - self.layer * 3, bg=self.background)
        frame.propagate(False)
        frame.place(x=x + self.layer * 5, y=y + self.layer * 3)
        frame.bind("<Button-1>", self.delete_box)
        frame.bind("<Enter>", self.add_hover)
        frame.bind("<Leave>", self.remove_hover)

        self.add_course_name(frame)
        self.add_course_id_and_group(frame)
        self.add_course_instructor(frame)
        return frame

    def add_hover(self, event):
        if self not in self.form.hovered:
            self.form.hovered.add(self)
            self.form.update_hovered()

    def remove_hover(self, event):
        self.form.hovered.remove(self)
        self.form.update_hovered()

    def calculate_position(self, day):
        pad_x = 1
        pad_y = 25 + 1
        # calculating top_left X
        x = (5 - self.course.days[day]) * self.default_block_width + pad_x
        y = (self.course.start[0] - 7) * self.default_block_height + int(
            (self.course.start[1] / 60) * self.default_block_height) + pad_y  # calculating top_left Y

        height = int(((self.course.end[0] * 60 + self.course.end[1]) - (
            self.course.start[0] * 60 + self.course.start[1])) / 60 * self.default_block_height)
        return x, y, height

    def delete_box(self, event):
        self.frame1.destroy()
        if self.frame2 is not None:
            self.frame2.destroy()
        if self in self.form.hovered:
            self.form.hovered.remove(self)
        if self in self.selected_courses:
            self.selected_courses.remove(self)
            self.form.save_added_courses()
            self.form.total_credits -= self.course.credit
            self.form.root.title(
                f"Course Crafter - {self.form.total_credits} Credits selected")

    def add_course_name(self, root):
        name_label = tk.Label(root, text=to_persian(self.course.name), font=(
            "Calibri", 11), bg=self.background, wraplength=self.default_block_width - 10)
        name_label.bind("<Button-1>", self.delete_box)
        name_label.pack(side="top")

    def add_course_id_and_group(self, root):
        id_group = tk.Label(root, text=f"{self.course.id} - {self.course.group}", font=(
            "Calibri", 9), bg=self.background)
        id_group.bind("<Button-1>", self.delete_box)
        id_group.pack(side="top")

    def add_course_instructor(self, root):
        instructor_label = tk.Label(root, text=to_persian(self.course.instructor), font=(
            "Calibri", 10), bg=self.background)
        instructor_label.bind("<Button-1>", self.delete_box)
        instructor_label.pack(side="bottom", pady=5)


class ScheduleForm:
    def __init__(self, root: tk.Tk, departments, courses):
        self.root = root
        self.root.title("Course Crafter")

        self.hovered_course_box = None  # For mouse hover
        self.departments = departments
        self.courses = courses
        self.showing_postgraduate = False

        self.total_credits = 0
        self.listbox_courses = []
        self.grid_courses = []
        self.selected_department = None
        self.selected_course = None

        self.canvas = tk.Canvas(self.root, width=1260, height=735)
        self.canvas.pack()

        self.hovered = set()  # For selected courses in the grid

        self.create_left_frame()
        self.create_right_frame()
        self.create_menu()
        self.load()
        self.root.mainloop()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        course_menu = tk.Menu(menu)
        menu.add_cascade(label="Course", menu=course_menu)
        course_menu.add_command(label="Get Finals", command=self.get_finals)
        course_menu.add_command(label="Show Table", command=self.show_table)

    def show_table(self):
        table_window = tk.Toplevel(self.root)
        table_window.title("Table")
        table_window.geometry("800x500")
        table = ttk.Treeview(table_window, columns=(
            "name", "group", "credit", "instructor", "final", "time"))
        table.heading("#0", text=to_persian("کد درس"), anchor='e')
        table.heading("name", text=to_persian("نام درس"), anchor='e')
        table.heading("group", text=to_persian("شماره گروه"), anchor='e')
        table.heading("credit", text=to_persian("تعداد واحد"), anchor='e')
        table.heading("instructor", text=to_persian("مدرس"), anchor='e')
        table.heading("final", text=to_persian("امتحان"), anchor='e')
        table.heading("time", text=to_persian("زمان"), anchor='e')
        table.column("#0", width=50, anchor='e')
        table.column("name", width=100, anchor='e')
        table.column("group", width=50, anchor='e')
        table.column("credit", width=50, anchor='e')
        table.column("instructor", width=100, anchor='e')
        table.column("final", width=50, anchor='e')
        table.column("time", width=100, anchor='e')
        table.pack(fill="both", expand=True)
        for _course in self.grid_courses:
            course = _course.course
            table.insert("", "end", text=course.id, values=(to_persian(course.name),
                         course.group, course.credit, to_persian(course.instructor), course.final, to_persian(course.time)))

    def get_finals(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("200x100")
        username_label = tk.Label(login_window, text="Username:")
        username_label.grid(row=0, column=0)
        username_entry = tk.Entry(login_window)
        username_entry.grid(row=0, column=1)
        password_label = tk.Label(login_window, text="Password:")
        password_label.grid(row=1, column=0)
        password_entry = tk.Entry(login_window, show="*")
        password_entry.grid(row=1, column=1)
        login_button = tk.Button(login_window, text="Login", command=lambda: self.get_finals_from_edu(
            username_entry.get(), password_entry.get(), login_window))
        login_button.grid(row=2, column=0, columnspan=2)

    def get_finals_from_edu(self, username, password, login_window):
        pbar = ttk.Progressbar(login_window, orient="horizontal",
                               length=200, mode="determinate", maximum=100, value=0)
        pbar.grid(row=3, column=0, columnspan=2)
        login_window.update()
        session = edu.login(username, password)
        if session is None:
            messagebox.showerror(
                "Error", "Wrong username or password.", icon="error")
            return
        th = threading.Thread(
            target=lambda: self.get_finals_after_login(session, pbar))
        th.start()

    def get_finals_after_login(self, session, pbar):
        global local_data
        for department in self.departments:
            courses = edu.get_finals_from_department(session, department.id)
            if courses is None:
                messagebox.showerror(
                    "Error", "Error getting courses.", icon="error")
                return
            pbar['value'] += 100 / len(self.departments)
            for course in self.courses:
                key = f'{course.id}-{course.group}-{course.credit}'
                if key in courses:
                    course.final = courses[key]
        local_data.courses = self.courses
        local_data.save()
        messagebox.showinfo("Done", "Done!", icon="info")

    def create_right_frame(self):
        self.days = ['پنجشنبه', 'چهار شنبه',
                     'سه شنبه', 'دوشنبه', 'یکشنبه', 'شنبه']

        # reshape each day
        self.days = [to_persian(day) for day in self.days]

        self.hours = list(range(7, 21))
        self.right_frame = tk.Frame(self.root)
        self.create_days(self.right_frame)
        self.right_frame.place(x=320, y=5)

    def create_days(self, root):
        self.grid_frame = tk.Frame(root)
        width = 150
        height = 50

        # putting days
        days_frame = tk.Frame(self.grid_frame)
        for i in range(len(self.days)):
            day_frame = tk.Frame(days_frame, width=width, height=height * 0.5)
            label = tk.Label(day_frame, text=self.days[i])
            label.pack(side="top", anchor="center")
            day_frame.propagate(False)
            day_frame.pack(side="left")
        # putting clock column
        clock_frame = tk.Frame(
            days_frame, width=width / 2, height=height * 0.3)
        clock_frame.pack(side="left")
        days_frame.pack(side="top")

        # putting other rows:
        for i in range(len(self.hours)):
            row_frame = tk.Frame(self.grid_frame)
            for j in range(len(self.days)):
                raw_frame = tk.Frame(row_frame, width=width, height=height,
                                     highlightbackground="white", highlightthickness=1)
                raw_frame.propagate(False)
                label = tk.Label(raw_frame)
                label.pack(side="top", anchor="center")
                raw_frame.pack(side="left")
            clock_frame = tk.Frame(row_frame, width=width / 2, height=height)
            label = tk.Label(clock_frame, text=f"{self.hours[i]}:00")
            label.pack(side="top", anchor="sw", pady=0)
            clock_frame.propagate(False)
            clock_frame.pack(side="left")
            row_frame.pack(side="top")

        self.grid_frame.pack(side="right")

    def create_left_frame(self):
        self.left_frame = tk.Frame(self.root, height=750, width=300)
        self.left_frame.place(x=10, y=10)

        self.create_left_first_row(self.left_frame)
        self.create_search_box(self.left_frame)
        self.create_listbox(self.left_frame)
        self.create_course_info(self.left_frame)

    def create_left_first_row(self, root):
        self.left_first_row = tk.Frame(root)

        self.create_checkbox(self.left_first_row)
        self.create_combo(self.left_first_row)

        self.left_first_row.pack(side="top")

    def create_checkbox(self, root):
        self.checkbox_var = tk.BooleanVar()
        self.checkbox_var.set(False)

        self.checkbox = tk.Checkbutton(
            root, text=to_persian("تحصیلات تکمیلی"), variable=self.checkbox_var,
            command=lambda: self.update_department())
        self.checkbox.pack(side="left")

    def create_combo(self, root):
        names = ["دانشکده را انتخاب کنید"]
        ids = []

        for department in self.departments:
            names.append(department.name)
            ids.append(department.id)

        # convert to persian
        names = [to_persian(name) for name in names]

        self.selected_item = tk.StringVar(value=names[0])
        self.combo = ttk.Combobox(
            root, values=names, textvariable=self.selected_item, justify="right", width=17)
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

        search_text = (self.search_entry.get().lower()).replace(
            'ك', 'ک').replace('ي', 'ی').split(' ')

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

        self.listbox = tk.Listbox(list_frame, selectmode=tk.NONE, font=(
            "Helvetica", 15), justify="right", height=22)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.listbox.pack(side="left", fill="both", padx=0, pady=0)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.config(command=self.listbox.yview, troughcolor="black")
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="both", padx=0)

        self.listbox.bind("<Motion>", self.on_hover_enter)
        self.listbox.bind("<Leave>", self.on_hover_exit)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Double-1>", self.add_course)

        list_frame.pack(side="top", fill="x", pady=5)

    def on_hover_enter(self, event):
        index = self.listbox.index("@%s,%s" % (event.x, event.y))
        if index >= 0:
            if self.hovered_course_box:
                if self.hovered_course_box.course.id != self.listbox_courses[index].id or \
                        self.hovered_course_box.course.group != self.listbox_courses[index].group:
                    self.hovered_course_box.delete_box(event)
                    self.hovered_course_box = None
            else:
                if not self.already_exist(self.listbox_courses[index]) and not (self.listbox_courses[index] == None or self.listbox_courses[index].time == ""):
                    self.hovered_course_box = CourseBox(
                        self.grid_frame, self.listbox_courses[index], self.grid_courses, self, layer=self.get_layer(self.listbox_courses[index]), is_hovered=True)

    def on_hover_exit(self, event):
        if self.hovered_course_box:
            self.hovered_course_box.delete_box(event)
        self.hovered_course_box = None

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
                          f"امتحان: {self.selected_course.final}\n" \
                          f"زمان کلاس: {self.selected_course.time}\n" \
                          f"توضیحات: {self.selected_course.details}\n" \
                          f"کلاس مجازی:\n{self.selected_course.virtual_class}"

            # Reshape the text
            course_info = to_persian(course_info)

            self.details_label.config(text=course_info)

    def create_course_info(self, root):
        self.course_info_frame = tk.Frame(root, height=230, width=290)
        self.course_info_frame.pack(side="top")
        self.details_label = tk.Label(
            self.course_info_frame, text=to_persian("اطلاعات درس"), anchor="e", justify="right", wraplength=270)
        self.details_label.place(x=0, y=0, width=290)

    def add_course(self, event=None):
        if self.selected_course == None or self.selected_course.time == "":
            messagebox.showerror(
                "Error",
                "The course does not have a specified time, if you think that the time is specified, delete the .cc files and run the program again.",
                icon="error")
            return
        if self.already_exist(self.selected_course):
            messagebox.showerror(
                "Error", "The course is already in the schedule.", icon="error")
            return
        course_box = CourseBox(
            self.grid_frame, self.selected_course, self.grid_courses, self, layer=self.get_layer(self.selected_course))
        self.grid_courses.append(course_box)
        self.save_added_courses()

    def get_layer(self, course):
        layer = 0
        for course_box in self.grid_courses:
            _course = course_box.course
            if Course.check_conflict(course, _course):
                layer = max(layer, course_box.layer + 1)
        return layer

    def update_hovered(self):
        if len(self.hovered) != 0:
            courses = sorted(list(self.hovered), key=lambda x: x.layer)
        else:
            courses = sorted(self.grid_courses, key=lambda x: x.layer)
        for course_box in courses:
            course_box.frame1.destroy()
            if course_box.frame2 is not None:
                course_box.frame2.destroy()
            course_box.frame1 = course_box.create_frame(0)
            course_box.frame2 = course_box.create_frame(1)

    def update_listbox(self):
        # Insert items into the Listbox
        for course in self.listbox_courses:
            # convert the name to persian
            self.listbox.insert(tk.END, to_persian(course.name)[:40])

    def save_added_courses(self):
        global local_data
        courses = []
        for course_box in self.grid_courses:
            courses.append(course_box.course)
        local_data.set_added_courses(courses)

    def save(self, event=None):
        self.save_added_courses()
        messagebox.showinfo("Done", "Saved succesfully!", icon="info")

    def load(self, event=None):
        global local_data
        local_data = ApplicationData.load()
        courses = local_data.added_courses
        for course in courses:
            if self.already_exist(course):
                continue
            if self.get_layer(course) > 0:
                course_box = CourseBox(
                    self.grid_frame, course, self.grid_courses, self, layer=self.get_layer(course))
            else:
                course_box = CourseBox(
                    self.grid_frame, course, self.grid_courses, self)
            self.grid_courses.append(course_box)


    def already_exist(self, course):
        for course_box in self.grid_courses:
            _course = course_box.course
            if _course.id == course.id and _course.group == course.group:
                return True
        return False


def to_persian(txt):
    # check if OS is mac or windows and not linux then return the text
    if os.name == "posix" and os.uname().sysname == "Linux":
        return get_display(arabic_reshaper.reshape(txt))
    return txt


def check_for_updated_courses(local_data: ApplicationData):
    """ Takes local saved data and compares it to online data, updates it if there's a mismatch """
    # TODO: Add to drop down menus
    try:
        updated_data = ApplicationData(*edu.get_department_and_courses())
    except:
        updated_data = local_data

    if not (local_data or updated_data):
        messagebox.showerror(
            "Error", 'No Local data or Internet connection, there is no data to show')
        return

    if not (local_data and local_data.is_data_uptodate(hash(updated_data))):
        added_courses = []
        if local_data:
            added_courses = local_data.added_courses
        local_data = updated_data
        local_data.set_added_courses(added_courses)
    return local_data


if __name__ == "__main__":
    try:
        # Reading saved information
        local_data = ApplicationData.load()
    except:
        local_data = None
    local_data = check_for_updated_courses(local_data)

    if local_data:
        # Run the app only if there is something to show
        departments, courses = local_data.data

        root = tk.Tk()
        root.minsize(1250, 750)
        app = ScheduleForm(root, departments, courses)
        
