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
    sign_up.title('Sign Up')
    img = Image.open("Images/GradebookMofficial.png")
    ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(50,50))

    header = ctk.CTkFrame(sign_up, height=50, fg_color='#36454F')
    header.pack(fill="x")
    image_label = ctk.CTkLabel(header, image=ctk_image, text="")
    image_label.place(x=50, y=0)
    ctk.CTkLabel(header, text="SIGN UP", font=('Arial', 20, 'bold'),text_color="white").place(x=150,y=10)

    ctk.CTkLabel(sign_up, text="Username:", font=('Arial', 12)).place(x=80, y=70)
    entry_user = ctk.CTkEntry(sign_up, width=300)
    entry_user.place(x=200, y=70)

    ctk.CTkLabel(sign_up, text="Password:", font=('Arial', 12)).place(x=80, y=140)
    entry_password = ctk.CTkEntry(sign_up, show="*", width=300)
    entry_password.place(x=200, y=140)

    ctk.CTkLabel(sign_up, text="Confirm Password:", font=('Arial', 12)).place(x=60, y=210)
    Confirm_password = ctk.CTkEntry(sign_up, show="*", width=300)
    Confirm_password.place(x=200, y=210)

    ctk.CTkButton(sign_up, text="Sign up", command=register, width=100).place(x=230, y=240)
    ctk.CTkButton(sign_up, text="Back to Login",width=100, command=lambda: [sign_up.destroy(), Login.logging_in()]).place(x=350, y=240)

    sign_up.mainloop()
