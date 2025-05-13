import customtkinter as ctk
from PIL import Image
from Main import *
import os
import csv

img1 = Image.open("Images/amascot.png")
ctk_image1 = ctk.CTkImage(light_image=img1, dark_image=img1, size=(500,350))
class_file = "classes.txt"
class_data = []
students = {}
selected_class = None
os.makedirs("data", exist_ok=True)

"""home"""

def home_content(content_home):
    for widget in content_home.winfo_children():
        widget.destroy()

    frame = ctk.CTkFrame(content_home, fg_color="#36454F", border_color="white", border_width=2)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    ctk.CTkLabel(frame, text="Welcome to GradeBook Manager", font=('Calibri', 40, 'bold')).pack(pady=40)

    mascot_label = ctk.CTkLabel(frame, image=ctk_image1, text="")
    mascot_label.pack(pady=10)

    ctk.CTkLabel(frame, text="Use the sidebar to manage students, grades, and classes.",
                font=('Calibri', 20)).pack(pady=10)

    return frame

"""This part is view student and grades sybau"""

def view_students(content_view):
    global students

    for widget in content_view.winfo_children():
        widget.destroy()

    frame = ctk.CTkFrame(content_view, fg_color="#36454F", border_color="white", border_width=2)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    ctk.CTkLabel(frame, text="Student Grades Viewer", font=('Calibri', 40, 'bold')).place(x=400, y=40)

    class_list = get_class_list()
    selectclass = ctk.CTkComboBox(frame, width=300, height=30, border_width=2, border_color="white")
    selectclass.place(x=450, y=100)

    if class_list:
        selectclass.set(class_list[0])

    scroll_frame = ctk.CTkFrame(frame, width=1000, height=500, border_width=2, border_color="white")
    scroll_frame.place(x=80, y=150)

    student_view = ctk.CTkTextbox(scroll_frame, width=1000, height=500, font=("Calibri", 20, "bold"))
    student_view.pack(padx=10, pady=10)

    def map_average_to_scale(avg, min_grade=0, max_grade=100, min_scale=5.0, max_scale=1.0):
        avg = max(min(avg, max_grade), min_grade)
        scale = max_scale - (avg - min_grade) / (max_grade - min_grade) * (max_scale - min_scale)

        scale = round(scale,1)

        if scale == 5.0:
            label = "Fail"
        elif scale == 3.0:
            label = "3A"
        elif 2.9 >= scale >= 1.0:
            label = "Pass"
        else:
            label = "No Grade"

        return scale, label

    def get_average(student_data):
        if 'grades' in student_data and student_data['grades']:
            grades = [float(grade) if isinstance(grade, str) else grade for grade in student_data['grades']]
            if grades:
                return sum(grades) / len(grades)
        return 0

    def refresh_lst():
        student_view.delete(1.0, "end")

        header = "Student ID - Name | Grades | Average | Rating"
        student_view.insert("end", header + "\n")
        student_view.insert("end", "=" * len(header) + "\n\n")

        if not students:
            student_view.insert("end", "No students found.\n")
            return

        for student_id, data in students.items():
            avg = get_average(data)
            scale, label = map_average_to_scale(avg)

            grades_display = str(data.get('grades', []))

            line = f"{student_id} - {data.get('name', 'Unknown')} | Grades: {grades_display} | Avg: {scale} | Grade Point: {label}"
            student_view.insert("end", line + "\n")
            student_view.insert("end", "-" * len(line) + "\n\n")

    def class_selected(choice):
        global selected_class
        selected_class = choice
        data_path = f"data/{selected_class}.csv"
        students.clear()
        students.update(load_students(data_path))
        refresh_lst()

    selectclass.configure(values=class_list, command=class_selected)

    if class_list:
        class_selected(class_list[0])

    return frame

"""This part is show student"""
def show_student(content_student):
    global students
    for widget in content_student.winfo_children():
        widget.destroy()

    frame = ctk.CTkFrame(content_student, fg_color="#36454F", border_color="white", border_width=2)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    ctk.CTkLabel(frame, text="Student Manager", font=('Calibri', 40, 'bold')).place(x=400, y=40)

    ctk.CTkLabel(frame, text="Enter Id:", font=('Calibri', 15)).place(x=200, y=100)
    entry_id = ctk.CTkEntry(frame, placeholder_text="Student ID", width=250, font=("Calibri", 16))
    entry_id.place(x=260, y=100)

    ctk.CTkLabel(frame, text="Enter Student:", font=('Calibri', 15)).place(x=170, y=140)
    entry_name = ctk.CTkEntry(frame, placeholder_text="Student name", width=250, font=("Calibri", 16))
    entry_name.place(x=260, y=140)

    ctk.CTkLabel(frame, text="Enter Grade:", font=('Calibri', 15)).place(x=520, y=100)
    entry_grade = ctk.CTkEntry(frame, placeholder_text="Grade", width=250, font=("Calibri", 16))
    entry_grade.place(x=610, y=100)

    def show_temp_message(parent, text, color="white", duration=3000):
        message = ctk.CTkLabel(parent, text=text, fg_color="transparent", text_color=color, font=('Calibri', 15))
        message.place(x=80, y=240)
        message.after(duration, message.destroy)

    def aadd_student():
        sid = entry_id.get().strip()
        name_input = entry_name.get().strip()

        if not sid or not name_input:
            show_temp_message(frame, "ID and Name are required", "red")
            return

        for student in students.values():
            if student['name'].lower() == name_input.lower():
                show_temp_message(frame, "Student name already exists", "red")
                return

        try:
            add_student(students, sid, name_input)
            refresh_lst()
            show_temp_message(frame, "Student added successfully", "green")
            clear_entries()
        except ValueError as e:
            show_temp_message(frame, str(e), "red")

    def aadd_grade():
        sid = entry_id.get().strip()
        try:
            grade = int(entry_grade.get().strip())
            if grade < 0 or grade > 100:
                raise ValueError("Grade must be between 0 and 100.")
            add_grade(students, sid, grade)
            refresh_lst()
            show_temp_message(frame, "Grade added", "green")
            clear_entries()
        except ValueError:
            show_temp_message(frame, "Invalid Grade or student", "red")

    def edit_student():
        sid = entry_id.get().strip()
        new_name = entry_name.get().strip()

        if not sid or not new_name:
            show_temp_message(frame, "ID and New Name are required", "red")
            return

        if sid not in students:
            show_temp_message(frame, "Student not found", "red")
            return

        students[sid]['name'] = new_name
        refresh_lst()
        show_temp_message(frame, "Student name updated", "green")
        clear_entries()

    def delete_student():
        sid = entry_id.get().strip()
        if not sid:
            show_temp_message(frame, "Enter Student ID to delete", "red")
            return

        if sid in students:
            del students[sid]
            refresh_lst()
            show_temp_message(frame, f"Student {sid} removed", "green")
            clear_entries()
        else:
            show_temp_message(frame, "Student not found", "red")

    def save():
        try:
            save_student(data_path, students)
            show_temp_message(frame, "Saved successfully!", "green")
        except Exception as e:
            show_temp_message(frame, f"Error: {str(e)}", "red")

    def clear_entries():
        entry_id.delete(0, 'end')
        entry_name.delete(0, 'end')
        entry_grade.delete(0, 'end')

    ctk.CTkButton(frame, text="Add Student", fg_color="transparent", border_color="white", border_width=2, width=80, command=aadd_student).place(x=260, y=180)
    ctk.CTkButton(frame, text="Add Grade", fg_color="transparent", border_color="white", border_width=2, width=80, command=aadd_grade).place(x=610, y=140)
    ctk.CTkButton(frame, text="Save", fg_color="transparent", border_color="white", border_width=2, width=80, command=save).place(x=780, y=180)

    ctk.CTkButton(frame, text="Edit", fg_color="transparent", border_color="white", border_width=2, width=60, command=edit_student).place(x=360, y=180)
    ctk.CTkButton(frame, text="Delete", fg_color="transparent", border_color="white", border_width=2, width=60, command=delete_student).place(x=450, y=180)

    scroll_frame = ctk.CTkFrame(frame, width=1000, height=400, border_width=2, border_color="white")
    scroll_frame.place(x=80, y=280)

    student_lst = ctk.CTkTextbox(scroll_frame, width=1000, height=400, font=("Calibri", 20, "bold"))
    student_lst.pack(padx=10, pady=10)

    def refresh_lst():
        student_lst.delete("1.0", "end")
        for student_id, data in students.items():
            avg = get_average(students, student_id)
            scale = average_scaling(avg)
            line = f"{student_id} - {data['name']} | Grades: {data['grades']} | Avg: {scale}"
            student_lst.insert("end", line + "\n")
            student_lst.insert("end", "-" * len(line) + "\n\n")

    if selected_class is None:
        return

    data_path = f"data/{selected_class}.csv"
    students = load_students(data_path)

    refresh_lst()

def add_student(student_dict, student_id, name):
    if student_id in student_dict:
        raise ValueError("Student ID already exists.")
    student_dict[student_id] = {'name': name, 'grades': []}

def add_grade(student_dict, student_id, grade):
    if student_id in student_dict:
        student_dict[student_id]['grades'].append(grade)
    else:
        raise ValueError("Student not found.")

def average_scaling(avg, min_grade = 0, max_grade =100,min_scale=5.0,max_scale=1.0):
    avg = max(min(avg, max_grade), min_grade)
    scale = max_scale - (avg - min_grade) / (max_grade - min_grade)*(max_scale - min_scale)
    return round(scale,1)


def get_average(student_dict, student_id):
    grades = student_dict.get(student_id, {}).get('grades', [])
    return sum(grades) / len(grades) if grades else 0

"""Data storage UWU"""
def save_student(filepath, student_dict):
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Id", "Name", "Grades","Average"])
        for sid, data in student_dict.items():
            grade_str = ",".join(map(str, data['grades']))
            avg = get_average(student_dict,sid)
            writer.writerow([sid, data['name'], grade_str, f"{avg:.2f}"])

def load_students(filepath):
    student_dict = {}
    try:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sid = row["Id"]
                name = row["Name"]
                grades = list(map(int, row["Grades"].split(','))) if row["Grades"] else []
                student_dict[sid] = {'name': name, 'grades': grades}
    except FileNotFoundError:
        pass
    return student_dict

"""functions classOsdas"""
def get_class_list():
    if os.path.exists(class_file):
        with open(class_file, "r") as f:
            return [line.strip() for line in f if line.strip()]
        return []

def load_classes():
    global class_data
    if os.path.exists(class_file):
        with open(class_file, "r") as f:
            class_data = [line.strip() for line in f if line.strip()]
    else:
        class_data = []

def save_all_classes():
    with open(class_file, "w") as f:
        for cls in class_data:
            f.write(cls + "\n")

def add_class(entry, display_frame):
    name = entry.get().strip().upper()
    if len(class_data)>5:
        limit_message(entry)
        return
    if name and name not in class_data:
        class_data.append(name)
        save_all_classes()
        entry.delete(0, 'end')
        update_class(display_frame)

def limit_message(entry):
    entry.delete(0, 'end')
    entry.insert(0, "Maximum limit of 6 class has reached")
    color = entry.cget("border_color")
    entry.configure(border_color="red")
    entry.after(1000,lambda: entry.configure(border_color=color))

def delete_class(display_frame):
    global selected_class
    if selected_class in class_data:
        class_data.remove(selected_class)
        selected_class = None
        save_all_classes()
        update_class(display_frame)

def rename_class(entry, display_frame):
    global selected_class
    new_name = entry.get().strip().upper()
    if selected_class and new_name and new_name not in class_data:
        index = class_data.index(selected_class)
        class_data[index] = new_name
        selected_class = None
        entry.delete(0, 'end')
        save_all_classes()
        update_class(display_frame)

def select_class(cls_name, display_frame):
    global selected_class
    selected_class = cls_name
    update_class(display_frame)
    show_student(display_frame.master.master)

def update_class(display_frame):
    for widget in display_frame.winfo_children():
        widget.destroy()
    header = ctk.CTkLabel(display_frame,text=f"Classes:({len(class_data)}/6)",font=('Calibri',20,'bold'),text_color="white",width=900)
    header.pack(anchor="w",padx=80,pady=10)

    if len(class_data) >= 5:
        warning = ctk.CTkLabel(display_frame,text=f"Warning: {1+5 - len(class_data)} slots remaining",font=('Calibri', 20),text_color="red")
        warning.pack(anchor='w', padx=10, pady=(0, 10))

    if not class_data:
        empty_class = ctk.CTkLabel(display_frame,text="No class available",font=('Calibri',20,'bold'),text_color="white")
        empty_class.pack(anchor="w",padx=20, pady=10)
        return

    for idx, cls in enumerate(class_data, 1):
        btn = ctk.CTkButton(
            display_frame,
            text=f"{idx}. {cls}",
            font=('Calibri', 16),
            border_width=2,
            border_color="white",
            width=300,height=40,
            fg_color="#2C2C2C" if cls != selected_class else "#5B8C5A",
            hover_color="#6C9A70",
            command=lambda c=cls: select_class(c, display_frame)
        )
        btn.pack(anchor='w', padx=10, pady=2, fill='x')

def show_class(content_class):
    for widget in content_class.winfo_children():
        widget.destroy()

    load_classes()

    screen_width = content_class.winfo_screenwidth()
    screen_height = content_class.winfo_screenheight()
    main_frame = ctk.CTkFrame(content_class, fg_color="transparent", height=screen_height-180, width=screen_width-250,border_color="white",border_width=2)
    main_frame.pack(fill="both", expand=True)

    title_label = ctk.CTkLabel(main_frame, text="THE CLASS", font=('Calibri', 50, 'bold'))
    title_label.place(x=440, y=60)

    entry = ctk.CTkEntry(main_frame, placeholder_text="Add a class",placeholder_text_color="white",font=('Calibri',20,'bold'), height=50,width=400)
    entry.place(x=300, y=120)

    display_frame = ctk.CTkFrame(main_frame, width=1180, height=400, fg_color="#536878",border_color="white",border_width=2)
    display_frame.place(x=50, y=250)

    add_btn = ctk.CTkButton(main_frame, text="Add",fg_color="transparent",border_color="white", border_width=2,hover_color="#6b828c", command=lambda: add_class(entry, display_frame),width=100,height=50)
    add_btn.place(x=700, y=120)

    rename_btn = ctk.CTkButton(main_frame, text="Rename",fg_color="transparent",border_color="white", border_width=2,hover_color="#6b828c", command=lambda: rename_class(entry, display_frame),width=100,height=50)
    rename_btn.place(x=400, y=190)

    delete_btn = ctk.CTkButton(main_frame, text="Delete",fg_color="transparent",border_color="white", border_width=2,hover_color="#6b828c", command=lambda: delete_class(display_frame),width=100,height=50)
    delete_btn.place(x=600, y=190)

    update_class(display_frame)