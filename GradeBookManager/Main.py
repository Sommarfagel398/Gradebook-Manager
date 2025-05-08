import customtkinter as ctk
from PIL import Image
import Login
from Functions import *
import os

def open_main(username):
    window = ctk.CTk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f'{screen_width}x{screen_height}')
    window.resizable(False, False)
    window.title('Grade Book Manager')
    img = Image.open("Images/GradebookMofficial.png")
    img1 = Image.open("Images/amascot.png")

    ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(100,100))
    ctk_image1 = ctk.CTkImage(light_image=img1, dark_image=img1, size=(500,350))

    """Header 🥀"""
    top = ctk.CTkFrame(window, fg_color=("#36454F"), width=screen_width, height=80,border_color="white",border_width=4)
    top.place(x=0, y=0)

    ctk.CTkLabel(top, text=f'Welcome to Grade Book Manager, {username}...',font=('Calibri', 40, 'bold'), text_color="white").place(x=15, y=15)
    ctk.CTkButton(top, text='Log out', fg_color="transparent",font=('Calibri',20), text_color="white",hover_color="#6b828c"
                  ,border_color="white",border_width=2, width=100, command=lambda: [window.destroy(), Login.logging_in()]).place(x=screen_width - 120, y=25)

    """side bar on left"""

    menu = ctk.CTkFrame(window, fg_color="#36454F", height=750, width=200, border_color="#D3D3D3", border_width=4)
    menu.place(x=20, y=100)

    image_label = ctk.CTkLabel(menu, image=ctk_image, text="")
    image_label.place(x=45, y=10)

    text_label = ctk.CTkLabel(menu, text="Gradebook Manager", text_color="white", font=('Calibri', 20, 'bold'))
    text_label.place(x=12, y=120)

    home_Button = ctk.CTkButton(menu, text='Home', fg_color="transparent", font=('Calibri', 20, 'bold'),
                                 text_color="white", height=50, width=170, hover_color="#6b828c",
                                 command=lambda: show_home(content))
    home_Button.place(x=15, y=180)

    grade_Button = ctk.CTkButton(menu,text='Grades',fg_color="transparent",font=('Calibri', 20, 'bold'),
                                 text_color="white",height=50,width=170,hover_color="#6b828c",command=lambda: show_grade(content))
    grade_Button.place(x=15, y=250)

    student_Button = ctk.CTkButton(menu,text='Student Grades',fg_color="transparent",font=('Calibri',20,'bold'),
                                   text_color="white",height=50,width=170,hover_color="#6b828c",command=lambda: show_student(content))
    student_Button.place(x=15,y=330)

    gradeEntry_Button = ctk.CTkButton(menu, text='Grade Entry', fg_color="transparent", font=('Calibri', 20, 'bold'),
                                      text_color="white",height=50, width=170, hover_color="#6b828c",command=lambda: show_gradeEntry(content))
    gradeEntry_Button.place(x=15, y=410)


    manage_Button = ctk.CTkButton(menu, text='Manage Grades', fg_color="transparent", font=('Calibri', 20, 'bold'),
                                  text_color="white",height=50, width=170, hover_color="#6b828c",command=lambda: show_manageGrade(content))
    manage_Button.place(x=15, y=500)

    class_Button = ctk.CTkButton(menu, text='Create a Class', fg_color="transparent", font=('Calibri', 20, 'bold'),
                                  text_color="white", height=50, width=170, hover_color="#6b828c",
                                  command=lambda: show_class(content))
    class_Button.place(x=15, y=590)

    """content is here"""
    content = ctk.CTkFrame(window, fg_color=("#36454F"),height=750,width=1180,border_color="white",border_width=4)
    content.place(x=240,y=100)

    content_label = ctk.CTkLabel(content, text="Soon...", font=('Calibri',50,'bold'))
    content_label.place(x=440,y=490)

    ctk.CTkLabel(content, text="nothing can be added yet...",font=('Calibri',20,'bold')).place(x=500,y=550)
    image_label2 = ctk.CTkLabel(content, image=ctk_image1, text="")
    image_label2.place(x=300, y=130)


    window.mainloop()