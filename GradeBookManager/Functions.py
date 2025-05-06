import customtkinter
import customtkinter as ctk
from PIL import Image
import Login
from openpyxl import load_workbook

img1 = Image.open("Images/amascot.png")
ctk_image1 = ctk.CTkImage(light_image=img1, dark_image=img1, size=(500,350))

"""Home butto"""
def show_home(content_home):
    for widget in content_home.winfo_children():
        widget.destroy

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
        widget.destroy

    ctk.CTkFrame(content_student, fg_color=("#36454F"), height=750, width=1180).place(x=240, y=100)
    ctk.CTkLabel(content_student, text="THE STUDENTS 🥀", font=('Calibri', 50, 'bold')).place(x=440, y=490)

"""grade entry button"""
def show_gradeEntry(content_entry):
    for widget in content_entry.winfo_children():
        widget.destroy

    ctk.CTkFrame(content_entry, fg_color=("#36454F"), height=750, width=1180).place(x=240, y=100)
    ctk.CTkLabel(content_entry, text="THE GRADE ENTRIES 🥀", font=('Calibri', 50, 'bold')).place(x=440, y=490)

"""Manage Grade"""
def show_manageGrade(content_manage):
    for widget in content_manage.winfo_children():
        widget.destroy

    ctk.CTkFrame(content_manage, fg_color=("#36454F"), height=750, width=1180).place(x=240, y=100)
    ctk.CTkLabel(content_manage, text="THE MANAGE GRADE 🥀", font=('Calibri', 50, 'bold')).place(x=440, y=490)