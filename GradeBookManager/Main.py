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
    window.configure(fg_color="#202121")
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

    menu = ctk.CTkFrame(window, fg_color="#36454F", height=screen_height-180, width=220, border_color="#D3D3D3", border_width=4)
    menu.place(x=20, y=100)

    image_label = ctk.CTkButton(menu,image=ctk_image,compound="top",text=" Gradebook Manager ",fg_color="transparent",font=('Calibri', 20, 'bold'),
                                text_color="white",height=50,width=170,hover_color="#6b828c",command=lambda : home_content(content))
    image_label.place(x=10, y=10)

    class_Button = ctk.CTkButton(menu, text="Class Management", fg_color="transparent", font=('Calibri', 20, 'bold'),
                                  text_color="white", height=50, width=170, hover_color="#6b828c",
                                  command=lambda: show_class(content))
    class_Button.place(x=20, y=180)

    student_Button = ctk.CTkButton(menu, text="Student Management", fg_color="transparent",
                                   font=('Calibri', 20, 'bold'),
                                   text_color="white", height=50, width=170, hover_color="#6b828c",
                                   command=lambda: show_student(content))
    student_Button.place(x=13, y=250)

    student_Button = ctk.CTkButton(menu, text=f"View Students \nand Grades", fg_color="transparent",
                                   font=('Calibri', 20, 'bold'),
                                   text_color="white", height=50, width=170, hover_color="#6b828c",
                                   command=lambda: view_students(content))
    student_Button.place(x=20, y=310)

    """content is here"""
    content = ctk.CTkFrame(window, fg_color=("#36454F"),height=screen_height - 180,width=screen_width-250,border_color="white",border_width=2)
    content.place(x=240,y=100)

    frame = ctk.CTkFrame(content, fg_color="#36454F", border_color="white", border_width=2)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    ctk.CTkLabel(frame, text="Welcome to GradeBook Manager", font=('Calibri', 40, 'bold')).pack(pady=40)

    mascot_label = ctk.CTkLabel(frame, image=ctk_image1, text="")
    mascot_label.pack(pady=10)

    ctk.CTkLabel(frame, text="Use the sidebar to manage students, grades, and classes.",
                 font=('Calibri', 20)).pack(pady=10)

    window.mainloop()