import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import Sign_up
import Main
from Functions import *

def logging_in():
    def login_attempt():
        username = entry_user.get()
        password = entry_password.get()
        success = False

        try:
            with open("users.txt", "r") as file:
                for line in file:
                    stored_user, stored_pass = line.strip().split(":")
                    if stored_user == username and stored_pass == password:
                        success = True
                        break
        except FileNotFoundError:
            with open("users.txt", "w") as file:
                pass
            messagebox.showerror("Error", "User database not found. A new one has been created.")
            return

        if success:
            user_folder = os.path.join("Users", username)

            data_folder = os.path.join(user_folder, "a_data_folder")
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

                class_file = os.path.join(data_folder, "classes.txt")

                if not os.path.exists(class_file):

                    try:
                        existing_updates_path = "updates/updates.txt"

                        if os.path.exists(existing_updates_path):
                            with open(existing_updates_path, "r") as source_file:
                                updates_content = source_file.read()
                            with open(os.path.join(user_folder, "updates.txt"), "w") as target_file:
                                target_file.write(updates_content)
                        else:
                            with open(os.path.join(user_folder, "updates.txt"), "w") as f:
                                f.write("Updates\n")

                    except Exception as e:
                        print(f"Error handling updates.txt: {e}")

            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            login.destroy()
            Main.open_main(username)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    login = ctk.CTk()
    login.geometry('680x300')
    login.resizable(False, False)
    login.configure(fg_color="#202121")
    login.title('Login')

    img = Image.open("Images/GradebookMofficial.png")
    ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(50, 50))
    img1 = Image.open("Images/ballsa.png")
    ctk_image1 = ctk.CTkImage(light_image=img1, dark_image=img1, size=(450, 250))

    frameright = ctk.CTkFrame(login, height=230, width=270, fg_color="transparent")
    frameright.place(x=400, y=60)
    image_masc = ctk.CTkLabel(frameright, image=ctk_image1, text="")
    image_masc.place(x=-90, y=-10)

    header = ctk.CTkFrame(login, height=50, fg_color='#323333')
    header.pack(fill="x")
    image_label = ctk.CTkLabel(header, image=ctk_image, text="")
    image_label.place(x=50, y=0)
    ctk.CTkLabel(header, text="WELCOME TO THE GRADE BOOK MANAGER", font=('Arial', 20, 'bold'),
                 text_color="white").place(x=150, y=10)

    ctk.CTkLabel(login, text="Username:", font=('Calibri', 20)).place(x=50, y=100)
    entry_user = ctk.CTkEntry(login, width=200)
    entry_user.place(x=150, y=100)

    ctk.CTkLabel(login, text="Password:", font=('Calibri', 20)).place(x=50, y=170)
    entry_password = ctk.CTkEntry(login, show="*", width=200)
    entry_password.place(x=150, y=170)

    ctk.CTkButton(login, text="Login", command=login_attempt, width=80,
                  fg_color="transparent", border_color="white", border_width=2, hover_color="#bdbdbd").place(x=150,
                                                                                                             y=250)
    ctk.CTkButton(login, text="Sign up",
                  command=lambda: [login.destroy(), Sign_up.open_signup()],
                  width=80, fg_color="transparent", border_color="white", border_width=2, hover_color="#bdbdbd").place(
        x=260, y=250)

    login.mainloop()

if __name__ == "__main__":
    logging_in()
