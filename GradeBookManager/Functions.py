import customtkinter
import customtkinter as ctk
from PIL import Image
import Login
from openpyxl import load_workbook
import os

img1 = Image.open("Images/amascot.png")
ctk_image1 = ctk.CTkImage(light_image=img1, dark_image=img1, size=(500,350))
class_file = "classes.txt"
class_data = []
selected_class = None

"""Home butto"""
def show_home(content_home):
    for widget in content_home.winfo_children():
        widget.destroy()

    ctk.CTkFrame(content_home, fg_color=("#36454F"), height=750, width=1180).place(x=240, y=100)
    ctk.CTkLabel(content_home, text="Coming soon...", font=('Calibri', 50, 'bold')).place(x=440, y=490)

    ctk.CTkLabel(content_home, text="nothing can be added yet", font=('Calibri', 20, 'bold')).place(x=500, y=550)
    ctk.CTkLabel(content_home, image=ctk_image1, text="").place(x=300, y=130)

"""Grade button"""
def show_grade(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    ctk.CTkFrame(content_frame, fg_color=("#36454F"), height=750, width=1180).place(x=240, y=100)
    ctk.CTkLabel(content_frame, text="THE GRADES 🥀", font=('Calibri', 50, 'bold')).place(x=440, y=490)

"""student button"""

def show_student(content_student):
    for widget in content_student.winfo_children():
        widget.destroy()

    ctk.CTkFrame(content_student, fg_color=("#36454F"), height=750, width=1180).place(x=240, y=100)
    ctk.CTkLabel(content_student, text="THE STUDENTS 🥀", font=('Calibri', 50, 'bold')).place(x=440, y=490)

"""grade entry button"""
def show_gradeEntry(content_entry):
    for widget in content_entry.winfo_children():
        widget.destroy()

    ctk.CTkFrame(content_entry, fg_color=("#36454F"), height=750, width=1180).place(x=240, y=100)
    ctk.CTkLabel(content_entry, text="THE GRADE ENTRIES 🥀", font=('Calibri', 50, 'bold')).place(x=440, y=490)

"""Manage Grade"""
def show_manageGrade(content_manage):
    for widget in content_manage.winfo_children():
        widget.destroy()

    ctk.CTkFrame(content_manage, fg_color=("#36454F"), height=750, width=1180).place(x=240, y=100)
    ctk.CTkLabel(content_manage, text="THE MANAGE GRADE 🥀", font=('Calibri', 50, 'bold')).place(x=440, y=490)

"""Class Function"""

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

def update_class(display_frame):
    for widget in display_frame.winfo_children():
        widget.destroy()
    header = ctk.CTkLabel(display_frame,text=f"Classes:({len(class_data)}/6)",font=('Calibri',20,'bold'),text_color="white",width=900)
    header.pack(anchor="w",padx=80,pady=10)

    if len(class_data) >= 5:
        warning = ctk.CTkLabel(
            display_frame,
            text=f"Warning: {1+5 - len(class_data)} slots remaining",
            font=('Calibri', 20),
            text_color="red"
        )
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

    main_frame = ctk.CTkFrame(content_class, fg_color="transparent", height=750, width=1180,border_color="white",border_width=4)
    main_frame.pack(fill="both", expand=True)

    title_label = ctk.CTkLabel(main_frame, text="THE CLASS 🥀", font=('Calibri', 50, 'bold'))
    title_label.place(x=440, y=60)

    entry = ctk.CTkEntry(main_frame, placeholder_text="Enter class name",placeholder_text_color="white",font=('Calibri',20,'bold'), height=50,width=400)
    entry.place(x=300, y=120)

    display_frame = ctk.CTkFrame(main_frame, width=1180, height=400, fg_color="#536878",border_color="white",border_width=2)
    display_frame.place(x=50, y=250)


    add_btn = ctk.CTkButton(main_frame, text="Add",fg_color="transparent",border_color="white",
                            border_width=2,hover_color="#6b828c",
                            command=lambda: add_class(entry, display_frame),width=100,height=50)
    add_btn.place(x=700, y=120)

    rename_btn = ctk.CTkButton(main_frame, text="Rename",fg_color="transparent",border_color="white",
                            border_width=2,hover_color="#6b828c",
                               command=lambda: rename_class(entry, display_frame),width=100,height=50)
    rename_btn.place(x=400, y=190)

    delete_btn = ctk.CTkButton(main_frame, text="Delete",fg_color="transparent",border_color="white",
                            border_width=2,hover_color="#6b828c",
                               command=lambda: delete_class(display_frame),width=100,height=50)
    delete_btn.place(x=600, y=190)

    update_class(display_frame)

    """https://github.com/Sommarfagel398/Gradebook-Manager.git"""