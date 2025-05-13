import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import Login

def open_signup():
    def register():
        username = entry_user.get()
        password = entry_password.get()
        confirm = Confirm_password.get()

        if not username or not password or not confirm:
            messagebox.showerror("Error", "Fill up all the fields.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords don't match.")
            return

        try:
            with open("users.txt", "r") as file:
                for line in file:
                    stored_user, _ = line.strip().split(":")
                    if stored_user == username:
                        messagebox.showerror("Error", "Username already exists.")
                        return
        except FileNotFoundError:
            pass

        with open("users.txt", "a") as file:
            file.write(f"{username}:{password}\n")

        messagebox.showinfo("Success", "Account has been created.")
        sign_up.destroy()
        Login.logging_in()

    sign_up = ctk.CTk()
    sign_up.geometry('680x300')
    sign_up.resizable(False, False)
    sign_up.configure(fg_color="#202121")
    sign_up.title('Sign Up')
    img = Image.open("Images/GradebookMofficial.png")
    ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(50,50))
    img1 = Image.open("Images/img_1.png")
    ctk_image1 = ctk.CTkImage(light_image=img1, dark_image=img1, size=(398, 340))


    frameright = ctk.CTkFrame(sign_up, height=230, width=250, fg_color="#0a0a0a",border_color="white",border_width=4)
    frameright.place(x=400, y=60)
    image_masc = ctk.CTkLabel(frameright, image=ctk_image1, text="")
    image_masc.place(x=0, y=0)

    header = ctk.CTkFrame(sign_up , height=50, fg_color='#323333')
    header.pack(fill="x")
    image_label = ctk.CTkLabel(header, image=ctk_image, text="")
    image_label.place(x=50, y=0)
    ctk.CTkLabel(header, text="Create a Account to log in 🗝️", font=('Arial', 20, 'bold'),text_color="white").place(x=150,y=10)

    ctk.CTkLabel(sign_up, text="Username:", font=('Calibri', 18)).place(x=80, y=80)
    entry_user = ctk.CTkEntry(sign_up, width=200)
    entry_user.place(x=180, y=80)

    ctk.CTkLabel(sign_up, text="Password:", font=('Calibri', 18)).place(x=80, y=130)
    entry_password = ctk.CTkEntry(sign_up, show="*", width=200)
    entry_password.place(x=180, y=130)

    ctk.CTkLabel(sign_up, text="Confirm Password:", font=('Calibri', 18)).place(x=20, y=190)
    Confirm_password = ctk.CTkEntry(sign_up, show="*", width=200)
    Confirm_password.place(x=180, y=190)

    ctk.CTkButton(sign_up, text="Sign up", command=register, width=80, fg_color="transparent",border_color="white",border_width=2,hover_color="#bdbdbd").place(x=180, y=250)
    ctk.CTkButton(sign_up, text="Back to Login",width=80,fg_color="transparent",border_color="white",border_width=2,hover_color="#bdbdbd",command=lambda: [sign_up.destroy(), Login.logging_in()]).place(x=280, y=250)

    sign_up.mainloop()
