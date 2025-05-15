import customtkinter as ctk
from PIL import Image
import os
import csv
import shutil
import tkinter as tk

img1 = Image.open("Images/amascot.png")
ctk_image1 = ctk.CTkImage(light_image=img1, dark_image=img1, size=(500, 350))
selected_class = None
students = {}

SUBJECTS = ["CC_APPSDEV", "CC_APPSDEV_LEC", "DATA_COMS", "DATA_STRUCT", "PLATECH", "QUAMETH", "DATA_STRUCT_LEC"]
"""home"""

def home_content(content_home, username):
    for widget in content_home.winfo_children():
        widget.destroy()

    frame = ctk.CTkFrame(content_home, fg_color="#36454F", border_color="white", border_width=2)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    ctk.CTkLabel(frame, text=f"Welcome to GradeBook Manager, {username}", font=('Calibri', 40, 'bold')).pack(pady=20)

    mascot_label = ctk.CTkLabel(frame, image=ctk_image1, text="")
    mascot_label.pack(pady=10)

    ctk.CTkLabel(frame, text="Use the sidebar to manage students, grades, and classes.",
                 font=('Calibri', 20)).pack(pady=10)

    log_frame = ctk.CTkFrame(frame, fg_color="#202121", border_color="white", border_width=1)
    log_frame.pack(pady=20, fill='both', expand=True, padx=40)
    ctk.CTkLabel(log_frame, text="Changelogs for fun", font=('Calibri', 24, 'bold')).pack(pady=10)
    log_text = ctk.CTkTextbox(log_frame, font=('Calibri', 16), height=300, wrap="word", fg_color="#4b4c4d")
    log_text.pack(padx=10, pady=10, fill="both", expand=True)

    try:
        with open(f"Users/{username}/updates.txt", "r", encoding="utf-8") as file:
            updates = file.read()
    except FileNotFoundError:
        updates = "No update log found. Make sure 'updates.txt' exists in your user directory."

    log_text.insert("end", updates)
    log_text.configure(state="disabled")

    return frame

""" view student and grades"""
def view_students(content_view, username):
    global students, selected_class

    for widget in content_view.winfo_children():
        widget.destroy()

    frame = ctk.CTkFrame(content_view, fg_color="#36454F", border_color="white", border_width=2)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    ctk.CTkLabel(frame, text="Student Grades Viewer", font=('Calibri', 40, 'bold')).place(x=400, y=40)

    class_list = get_class_list(username)
    selectclass = ctk.CTkComboBox(frame, fg_color="#202121", width=300, height=30,
                                  border_width=2, border_color="white")
    selectclass.place(x=450, y=100)

    status_label = ctk.CTkLabel(frame, text="", font=('Calibri', 14))
    status_label.place(x=450, y=130)

    scroll_frame = ctk.CTkFrame(frame, fg_color="#202121", width=1000, height=500,
                                border_width=2, border_color="white")
    scroll_frame.place(x=80, y=150)

    student_view = ctk.CTkTextbox(scroll_frame, fg_color="#202121", width=1000, height=500,
                                  font=("Calibri", 20, "bold"))
    student_view.pack(padx=10, pady=10)

    def refresh_lst():
        student_view.delete("1.0", "end")

        header = "Student ID - Name | Subjects | Grades | Average | Rating | Grade Point"
        student_view.insert("end", header + "\n")
        student_view.insert("end", "=" * len(header) + "\n\n")

        if not students:
            student_view.insert("end", "No students found.\n")
            return

        for student_id, data in students.items():
            avg = get_average(students, student_id)
            scale = average_scaling(avg)
            label = get_scale_label(scale)
            grades_display = []
            for grade_item in data['grades']:
                if isinstance(grade_item, dict):
                    grades_display.append(f"{grade_item['subject']}: {grade_item['grade']}")
                else:
                    grades_display.append(str(grade_item))

            line = f"{student_id} - {data.get('name', 'Unknown')} | "
            line += f"Subjects: {len(data['grades'])}/7 | "
            line += f"Grades: {', '.join(grades_display)} | "
            line += f"Avg: {avg:.2f} | "
            line += f"Scale: {scale} | "
            line += f"Grade Point: {label}"

            student_view.insert("end", line + "\n")
            student_view.insert("end", "-" * len(line) + "\n\n")

    def class_selected(choice):
        global selected_class
        selected_class = choice
        status_label.configure(text=f"Selected class: {choice}")
        data_path = f"Users/{username}/a_data_folder/{selected_class}.csv"
        students.clear()
        loaded_students = load_students(data_path)
        students.update(loaded_students)

        status_label.configure(text=f"Loaded {len(loaded_students)} students from {selected_class}")

        refresh_lst()

"""This part is show student"""

def show_student(content_student, username):
    global students, selected_class

    for widget in content_student.winfo_children():
        widget.destroy()

    frame = ctk.CTkFrame(content_student, fg_color="#36454F", border_color="white", border_width=2)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    ctk.CTkLabel(frame, text="Student Manager", font=('Calibri', 40, 'bold')).place(x=400, y=40)

    def validate_number(value):
        if value == "":
            return True
        return value.isdigit()

    def validate_text(value):
        if value == "":
            return True
        return all(c.isalpha() or c.isspace() for c in value)

    def validate_grades(value):
        if value == "":
            return True
        return all(c.isdigit() or c in [',', ' '] for c in value)

    validate_num_cmd = frame.register(validate_number)
    validate_txt_cmd = frame.register(validate_text)
    validate_grade_cmd = frame.register(validate_grades)

    ctk.CTkLabel(frame, text="Enter Id:", font=('Calibri', 15)).place(x=200, y=100)
    entry_id = ctk.CTkEntry(frame, fg_color="#202121", placeholder_text="Student ID",
                            width=250, font=("Calibri", 16))
    entry_id.configure(validate="key", validatecommand=(validate_num_cmd, '%P'))
    entry_id.place(x=260, y=100)

    ctk.CTkLabel(frame, text="Enter Student:", font=('Calibri', 15)).place(x=170, y=140)
    entry_name = ctk.CTkEntry(frame, fg_color="#202121", placeholder_text="Student name",
                              width=250, font=("Calibri", 16))
    entry_name.configure(validate="key", validatecommand=(validate_txt_cmd, '%P'))
    entry_name.place(x=260, y=140)

    ctk.CTkLabel(frame, text="Subject:", font=('Calibri', 15)).place(x=520, y=100)
    subject_var = ctk.StringVar(value=SUBJECTS[0])
    subject_dropdown = ctk.CTkOptionMenu(frame, fg_color="#202121", values=SUBJECTS,
                                         variable=subject_var, width=180, font=("Calibri", 16))
    subject_dropdown.place(x=580, y=100)

    ctk.CTkLabel(frame, text="Grade:", font=('Calibri', 15)).place(x=520, y=140)
    entry_grade = ctk.CTkEntry(frame, fg_color="#202121", placeholder_text="Enter grade (0-100)",
                               width=180, font=("Calibri", 16))
    entry_grade.configure(validate="key", validatecommand=(validate_grade_cmd, '%P'))
    entry_grade.place(x=580, y=140)

    def show_temp_message(parent, text, color="white", duration=3000):
        message = ctk.CTkLabel(parent, text=text, fg_color="transparent", text_color=color, font=('Calibri', 15))
        message.place(x=80, y=240)
        message.after(duration, message.destroy)

    def aadd_student():
        sid = entry_id.get().strip()
        name_input = entry_name.get().strip()

        if not sid or not name_input:
            show_temp_message(frame, "ID and Name are required", "white")
            return
        if sid in students:
            show_temp_message(frame, "Student ID already exists", "white")
            return

        for student in students.values():
            if student['name'].lower() == name_input.lower():
                show_temp_message(frame, "Student name already exists", "white")
                return
        try:
            add_student(students, sid, name_input)
            refresh_lst()
            show_temp_message(frame, "Student added successfully", "white")
            clear_entries()
        except ValueError as e:
            show_temp_message(frame, str(e), "white")

    def aadd_grade():
        sid = entry_id.get().strip()
        grade_str = entry_grade.get().strip()
        subject = subject_var.get()

        if not sid or not grade_str:
            show_temp_message(frame, "ID and grade required", "white")
            return

        if sid not in students:
            show_temp_message(frame, "Student ID not found", "white")
            return

        for grade_entry in students[sid]['grades']:
            if isinstance(grade_entry, dict) and grade_entry['subject'] == subject:
                show_temp_message(frame, f"Student already has a grade for {subject}", "white")
                return

        if len(students[sid]['grades']) >= 7:
            show_temp_message(frame, "Maximum 7 subjects allowed", "white")
            return

        try:
            grade = int(grade_str)
            if grade < 0 or grade > 100:
                raise ValueError("Grade must be between 0 and 100")

            add_grade_with_subject(students, sid, subject, grade)
            refresh_lst()
            show_temp_message(frame, f"Added grade {grade} for {subject}", "white")
            entry_grade.delete(0, 'end')
        except ValueError as e:
            show_temp_message(frame, f"Error: {str(e)}", "white")

    def edit_student():
        sid = entry_id.get().strip()
        new_name = entry_name.get().strip()

        if not sid or not new_name:
            show_temp_message(frame, "ID and new name are required", "white")
            return

        if sid not in students:
            show_temp_message(frame, "Student not found", "white")
            return

        students[sid]['name'] = new_name
        refresh_lst()
        show_temp_message(frame, "Student name updated", "white")
        clear_entries()

    def delete_student():
        sid = entry_id.get().strip()
        if not sid:
            show_temp_message(frame, "Enter Student ID to delete", "white")
            return

        if sid in students:
            del students[sid]
            refresh_lst()
            show_temp_message(frame, f"Student {sid} removed", "white")
            clear_entries()
        else:
            show_temp_message(frame, "Student not found", "white")

    def save():
        if selected_class is None:
            show_temp_message(frame, "No class selected", "white")
            return

        try:
            data_path = f"Users/{username}/a_data_folder/{selected_class}.csv"
            save_student(data_path, students)
            show_temp_message(frame, "Saved successfully!", "white")
        except Exception as e:
            show_temp_message(frame, f"Failed to save: {str(e)}", "white")

    def clear_entries():
        entry_id.delete(0, 'end')
        entry_name.delete(0, 'end')
        entry_grade.delete(0, 'end')

    def autofill_name(event):
        sid = entry_id.get().strip()
        if sid in students:
            entry_name.delete(0, 'end')
            entry_name.insert(0, students[sid]['name'])

    entry_id.bind("<KeyRelease>", autofill_name)

    ctk.CTkButton(frame, text="Add Student", fg_color="transparent", border_color="white", border_width=2, width=80,
                  command=aadd_student).place(x=260, y=180)
    ctk.CTkButton(frame, text="Add Grade", fg_color="transparent", border_color="white", border_width=2, width=80,
                  command=aadd_grade).place(x=780, y=140)
    ctk.CTkButton(frame, text="Save", fg_color="transparent", border_color="white", border_width=2, width=80,
                  command=save).place(x=780, y=180)

    ctk.CTkButton(frame, text="Edit", fg_color="transparent", border_color="white", border_width=2, width=60,
                  command=edit_student).place(x=360, y=180)
    ctk.CTkButton(frame, text="Delete", fg_color="transparent", border_color="white", border_width=2, width=60,
                  command=delete_student).place(x=450, y=180)

    scroll_frame = ctk.CTkFrame(frame, width=1000, height=400, border_width=2, border_color="white")
    scroll_frame.place(x=80, y=280)

    student_lst = ctk.CTkTextbox(scroll_frame, width=1000, height=400, font=("Calibri", 20, "bold"))
    student_lst.pack(padx=10, pady=10)

    def refresh_lst():
        student_lst.configure(state="normal")
        student_lst.delete("1.0", "end")

        for student_id, data in students.items():
            grades_display = []
            for grade_item in data['grades']:
                if isinstance(grade_item, dict):
                    grades_display.append(f"{grade_item['subject']}: {grade_item['grade']}")
                else:
                    grades_display.append(str(grade_item))

            avg = get_average(students, student_id)
            scale = grade_to_scale(avg)

            line = f"{student_id} - {data['name']} | Subjects: {len(data['grades'])}/7 | "
            line += f"Grades: {', '.join(grades_display)} | Avg: {avg:.2f} | Scale: {scale}"

            student_lst.insert("end", line + "\n")
            student_lst.insert("end", "-" * len(line) + "\n\n")

        student_lst.configure(state="disabled")

    if selected_class is None:
        class_list = get_class_list(username)
        if class_list:
            selected_class = class_list[0]
        else:
            show_temp_message(frame, "No classes available. Please create a class first.", "white")
            return frame

    data_path = f"Users/{username}/a_data_folder/{selected_class}.csv"
    students = load_students(data_path)
    refresh_lst()

    return frame

def add_student(student_dict, student_id, name):
    if student_id in student_dict:
        raise ValueError("Student ID already exists.")
    student_dict[student_id] = {'name': name, 'grades': []}

def add_grade_with_subject(student_dict, student_id, subject, grade):
    if student_id in student_dict:
        student_dict[student_id]['grades'].append({'subject': subject, 'grade': grade})
    else:
        raise ValueError("Student not found.")

def add_grade(student_dict, student_id, grade):
    if student_id in student_dict:
        student_dict[student_id]['grades'].append(grade)
    else:
        raise ValueError("Student not found.")


def average_scaling(avg, min_grade=0, max_grade=100, max_scale=1.0, min_scale=5.0):
    avg = max(min(avg, max_grade), min_grade)
    proportion = (avg - min_grade) / (max_grade - min_grade)
    scale = min_scale - proportion * (min_scale - max_scale)
    return round(scale, 1)

def grade_to_scale(grade):
    if grade >= 90:
        return 1.0
    elif grade >= 85:
        return 1.5
    elif grade >= 80:
        return 2.0
    elif grade >= 75:
        return 2.5
    elif grade >= 70:
        return 3.0
    elif grade >= 65:
        return 3.5
    elif grade >= 60:
        return 4.0
    else:
        return 5.0

def get_average(student_dict, student_id):
    if student_id not in student_dict:
        return 0

    grades = []
    for grade_item in student_dict[student_id]['grades']:
        if isinstance(grade_item, dict):
            grades.append(grade_item['grade'])
        else:
            grades.append(grade_item)

    if not grades:
        return 0

    try:
        return sum(grades) / len(grades)
    except ZeroDivisionError:
        return 0

"""Storage parts"""
def save_student(filepath, student_dict):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Id", "Name"] + SUBJECTS + ["Average", "Scale", "Grade Point"])

        for sid, data in student_dict.items():
            row = [sid, data['name']]
            subject_grades = {subject: "" for subject in SUBJECTS}

            for grade_item in data['grades']:
                if isinstance(grade_item, dict):
                    subject = grade_item['subject']
                    if subject in subject_grades:
                        subject_grades[subject] = str(grade_item['grade'])

            for subject in SUBJECTS:
                row.append(subject_grades[subject])

            avg = get_average(student_dict, sid)
            scale = grade_to_scale(avg)
            label = get_scale_label(scale)

            row.append(f"{avg:.2f}")
            row.append(f"{scale:.1f}")
            row.append(label)

            writer.writerow(row)

def load_students(filepath):
    student_dict = {}
    try:
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            subject_indices = {}
            for i, col in enumerate(header):
                if col in SUBJECTS:
                    subject_indices[col] = i
            for row in reader:
                if len(row) < 2:
                    continue
                sid = row[0]
                name = row[1]
                student_dict[sid] = {'name': name, 'grades': []}
                for subject, idx in subject_indices.items():
                    if idx < len(row) and row[idx].strip():
                        try:
                            grade = int(row[idx])
                            student_dict[sid]['grades'].append({'subject': subject, 'grade': grade})
                        except ValueError:
                            pass
    except FileNotFoundError:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Id", "Name"] + SUBJECTS + ["Average"])

    return student_dict


def create_student_view_textbox(parent):
    student_view = ctk.CTkTextbox(
        parent,
        fg_color="#202121",
        text_color="white",
        width=1000,
        height=500,
        font=("Calibri", 20, "bold"),
        border_width=1,
        border_color="#4a4a4a"
    )

    student_view._textbox.configure(
        disabledbackground="#202121",
        disabledforeground="white"
    )

    return student_view

def view_students(content_view, username):
    global students, selected_class

    for widget in content_view.winfo_children():
        widget.destroy()

    frame = ctk.CTkFrame(content_view, fg_color="#36454F", border_color="white", border_width=2)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    ctk.CTkLabel(frame, text="Student Grades Viewer", font=('Calibri', 40, 'bold')).place(x=400, y=40)

    class_list = get_class_list(username)
    selectclass = ctk.CTkComboBox(frame, fg_color="#202121", width=300, height=30, border_width=2, border_color="white")
    selectclass.place(x=450, y=100)

    if class_list:
        selectclass.set(class_list[0])

    scroll_frame = ctk.CTkFrame(frame, fg_color="#202121", width=1000, height=500, border_width=2, border_color="white")
    scroll_frame.place(x=80, y=150)

    student_view = create_student_view_textbox(scroll_frame)
    student_view.pack(padx=10, pady=10)

    def refresh_lst():
        student_view.configure(state="normal")
        student_view.delete("1.0", "end")

        header = "Student ID - Name | Subjects | Grades | Average | Scale | Grade Point"
        student_view.insert("end", header + "\n")
        student_view.insert("end", "=" * len(header) + "\n\n")

        if not students:
            student_view.insert("end", "No students found.\n")
            student_view.configure(state="disabled")
            return

        for student_id, data in students.items():
            avg = get_average(students, student_id)
            scale = grade_to_scale(avg)
            label = get_scale_label(scale)

            grades_display = []
            for grade_item in data['grades']:
                if isinstance(grade_item, dict):
                    grades_display.append(f"{grade_item['subject']}: {grade_item['grade']}")
                else:
                    grades_display.append(str(grade_item))

            line = f"{student_id} - {data.get('name', 'Unknown')} | "
            line += f"Subjects: {len(data['grades'])}/7 | "
            line += f"Grades: {', '.join(grades_display)} | "
            line += f"Avg: {avg:.2f} | "
            line += f"Scale: {scale} | "
            line += f"Grade Point: {label}"

            student_view.insert("end", line + "\n")
            student_view.insert("end", "-" * len(line) + "\n\n")

        student_view.configure(state="disabled")

    def class_selected(choice):
        global selected_class
        selected_class = choice
        data_path = f"Users/{username}/a_data_folder/{selected_class}.csv"
        students.clear()
        students.update(load_students(data_path))
        refresh_lst()

    selectclass.configure(values=class_list, command=class_selected)


    if class_list:
        selectclass.configure(values=class_list, command=class_selected)
        selectclass.set(class_list[0])
        class_selected(class_list[0])
    else:
        student_view.delete("1.0", "end")
        student_view.insert("end", "No classes available. Please create a class first.\n")

    return frame


def create_student_view_textbox(parent):
    student_view = ctk.CTkTextbox(
        parent,
        fg_color="#202121",
        text_color="white",
        width=1000,
        height=500,
        font=("Calibri", 20, "bold"),
        border_width=1,
        border_color="#4a4a4a"
    )

    try:
        student_view._textbox.configure(
            insertbackground="white",
            selectbackground="#4a6cd4",
            selectforeground="white"
        )
        try:
            student_view._textbox.configure(
                disabledbackground="#202121",
                disabledforeground="white"
            )
        except tk.TclError:
            pass

    except Exception as e:
        print(f"Warning: Could not fully configure text styling: {e}")

    return student_view

def debug_class_data(username):
    class_file = f"Users/{username}/a_data_folder/classes.txt"
    print(f"Checking class file: {class_file}")

    if os.path.exists(class_file):
        with open(class_file, "r") as f:
            classes = [line.strip() for line in f if line.strip()]
        print(f"Found {len(classes)} classes: {classes}")

        for cls in classes:
            data_path = f"Users/{username}/a_data_folder/{cls}.csv"
            print(f"  Checking file: {data_path}")
            if os.path.exists(data_path):
                try:
                    with open(data_path, 'r') as f:
                        reader = csv.reader(f)
                        header = next(reader, None)
                        row_count = sum(1 for _ in reader)
                    print(f"    File exists with {row_count} students")
                    print(f"    Header: {header}")
                except Exception as e:
                    print(f"    Error reading file: {e}")
            else:
                print(f"    File does not exist")
    else:
        print("Class file does not exist")

def get_subject_scale(subject_grade):
    return grade_to_scale(subject_grade)

def get_subject_scales(student_dict, student_id):
    subject_scales = {}

    if student_id in student_dict:
        for grade_item in student_dict[student_id]['grades']:
            if isinstance(grade_item, dict):
                subject = grade_item['subject']
                grade = grade_item['grade']
                scale = average_scaling(grade)  # Convert individual grade to scale
                subject_scales[subject] = scale

    return subject_scales

def get_scale_label(scale):
    if scale <= 1.0:
        return "Pass"
    elif scale <= 1.5:
        return "Pass"
    elif scale <= 2.0:
        return "Pass"
    elif scale <= 2.5:
        return "Pass"
    elif scale <= 3.0:
        return "Pass"
    elif scale <= 4.0:
        return "Fail"
    else:
        return "Fail"

def grade_to_scale(grade):
    if grade >= 90:
        return 1.0
    elif grade >= 85:
        return 1.5
    elif grade >= 80:
        return 2.0
    elif grade >= 75:
        return 2.5
    elif grade >= 70:
        return 3.0
    elif grade >= 65:
        return 3.5
    elif grade >= 60:
        return 4.0
    else:
        return 5.0

"""data storage functions3214"""
def save_student(filepath, student_dict):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Id", "Name"] + SUBJECTS + ["Average", "Scale", "Grade Point"])  # Added Scale and Grade Point columns

        for sid, data in student_dict.items():
            row = [sid, data['name']]

            subject_grades = {subject: "" for subject in SUBJECTS}

            for grade_item in data['grades']:
                if isinstance(grade_item, dict):
                    subject = grade_item['subject']
                    if subject in subject_grades:
                        subject_grades[subject] = str(grade_item['grade'])

            for subject in SUBJECTS:
                row.append(subject_grades[subject])

            avg = get_average(student_dict, sid)
            scale = average_scaling(avg)
            grade_point = get_scale_label(scale)

            row.append(f"{avg:.2f}")
            row.append(f"{scale}")
            row.append(grade_point)
            writer.writerow(row)

def load_students(filepath):
    student_dict = {}
    try:
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)

            subject_indices = {}
            for i, col in enumerate(header):
                if col in SUBJECTS:
                    subject_indices[col] = i

            for row in reader:
                if len(row) < 2:
                    continue
                sid = row[0]
                name = row[1]
                student_dict[sid] = {'name': name, 'grades': []}
                for subject, idx in subject_indices.items():
                    if idx < len(row) and row[idx].strip():
                        try:
                            grade = int(row[idx])
                            student_dict[sid]['grades'].append({'subject': subject, 'grade': grade})
                        except ValueError:
                            pass

    except FileNotFoundError:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Id", "Name"] + SUBJECTS + ["Average", "Scale", "Grade Point"])  # Include new columns here too

    return student_dict
"""functions sa class management"""

def get_class_list(username):
    class_file = f"Users/{username}/a_data_folder/classes.txt"
    if os.path.exists(class_file):
        with open(class_file, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def load_classes(username):
    class_file = f"Users/{username}/a_data_folder/classes.txt"
    class_data = []
    if os.path.exists(class_file):
        with open(class_file, "r") as f:
            class_data = [line.strip() for line in f if line.strip()]
    else:
        os.makedirs(os.path.dirname(class_file), exist_ok=True)
        with open(class_file, "w") as f:
            pass
    return class_data

def save_all_classes(username, class_data):
    class_file = f"Users/{username}/a_data_folder/classes.txt"
    os.makedirs(os.path.dirname(class_file), exist_ok=True)
    with open(class_file, "w") as f:
        for cls in class_data:
            f.write(cls + "\n")

def add_class(entry, display_frame, username):
    name = entry.get().strip().upper()
    class_data = load_classes(username)

    if len(class_data) > 5:
        limit_message(entry)
        return
    if name and name not in class_data:
        class_data.append(name)
        save_all_classes(username, class_data)
        entry.delete(0, 'end')
        update_class(display_frame, username)

def limit_message(entry):
    entry.delete(0, 'end')
    entry.insert(0, "Maximum limit of 6 classes has been reached")
    color = entry.cget("border_color")
    entry.configure(border_color="red")
    entry.after(1000, lambda: entry.configure(border_color=color))


def delete_class(display_frame, username):
    global selected_class
    class_data = load_classes(username)
    if selected_class in class_data:
        class_data.remove(selected_class)
        class_folder = f"Users/{username}/a_data_folder/{selected_class}"
        if os.path.exists(class_folder):
            try:
                shutil.rmtree(class_folder)
                print(f"Successfully removed class folder: {class_folder}")
            except Exception as e:
                print(f"Error removing class folder: {e}")
        selected_class = None
        save_all_classes(username, class_data)
        update_class(display_frame, username)

def rename_class(entry, display_frame, username):
    global selected_class
    new_name = entry.get().strip().upper()
    class_data = load_classes(username)

    if selected_class and new_name and new_name not in class_data:
        index = class_data.index(selected_class)
        class_data[index] = new_name
        selected_class = None
        entry.delete(0, 'end')
        save_all_classes(username, class_data)
        update_class(display_frame, username)

def select_class(cls_name, display_frame, username):
    global selected_class
    selected_class = cls_name
    update_class(display_frame, username)
    show_student(display_frame.master.master, username)

def update_class(display_frame, username):
    class_data = load_classes(username)

    for widget in display_frame.winfo_children():
        widget.destroy()
    header = ctk.CTkLabel(display_frame, text=f"Classes:({len(class_data)}/6)", font=('Calibri', 20, 'bold'),
                          text_color="white", width=900)
    header.pack(anchor="w", padx=80, pady=10)

    if len(class_data) >= 5:
        warning = ctk.CTkLabel(display_frame, text=f"Warning: {1 + 5 - len(class_data)} slots remaining",
                               font=('Calibri', 20), text_color="red")
        warning.pack(anchor='w', padx=10, pady=(0, 10))

    if not class_data:
        empty_class = ctk.CTkLabel(display_frame, text="No class available", font=('Calibri', 20, 'bold'),
                                   text_color="white")
        empty_class.pack(anchor="w", padx=20, pady=10)
        return

    for idx, cls in enumerate(class_data, 1):
        btn = ctk.CTkButton(
            display_frame,
            text=f"{idx}. {cls}",
            font=('Calibri', 16),
            border_width=2,
            border_color="white",
            width=300, height=40,
            fg_color="#2C2C2C" if cls != selected_class else "#5B8C5A",
            hover_color="#6C9A70",
            command=lambda c=cls: select_class(c, display_frame, username)
        )
        btn.pack(anchor='w', padx=10, pady=2, fill='x')


def show_class(content_class, username):
    for widget in content_class.winfo_children():
        widget.destroy()

    class_data = load_classes(username)

    screen_width = content_class.winfo_screenwidth()
    screen_height = content_class.winfo_screenheight()
    main_frame = ctk.CTkFrame(content_class, fg_color="transparent", height=screen_height - 180,
                              width=screen_width - 250, border_color="white", border_width=2)
    main_frame.pack(fill="both", expand=True)

    title_label = ctk.CTkLabel(main_frame, text="THE CLASS", font=('Calibri', 50, 'bold'))
    title_label.place(x=440, y=60)

    entry = ctk.CTkEntry(main_frame, fg_color="#202121", placeholder_text="Add a class", placeholder_text_color="white",
                         font=('Calibri', 20, 'bold'), height=50, width=400)
    entry.place(x=300, y=120)

    display_frame = ctk.CTkFrame(main_frame, width=1180, height=400, fg_color="#536878", border_color="white",
                                 border_width=2)
    display_frame.place(x=50, y=250)

    add_btn = ctk.CTkButton(main_frame, text="Add", fg_color="transparent", border_color="white", border_width=2,
                            hover_color="#6b828c",
                            command=lambda: add_class(entry, display_frame, username), width=100, height=50)
    add_btn.place(x=700, y=120)

    rename_btn = ctk.CTkButton(main_frame, text="Rename", fg_color="transparent", border_color="white", border_width=2,
                               hover_color="#6b828c",
                               command=lambda: rename_class(entry, display_frame, username), width=100, height=50)
    rename_btn.place(x=400, y=190)

    delete_btn = ctk.CTkButton(main_frame, text="Delete", fg_color="transparent", border_color="white", border_width=2,
                               hover_color="#6b828c",
                               command=lambda: delete_class(display_frame, username), width=100, height=50)
    delete_btn.place(x=600, y=190)


    update_class(display_frame, username)

    return main_frame