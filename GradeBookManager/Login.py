import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import Sign_up
import Main

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
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            login.destroy()
            Main.open_main(username)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")


    login = ctk.CTk()
    login.geometry('680x300')
    login.resizable(False, False)
    login.title('Login')
    img = Image.open("Images/GradebookMofficial.png")
    ctk_image = ctk.CTkImage(light_image=img,dark_image=img,size=(50,50))


    header = ctk.CTkFrame(login, height=50, fg_color='#36454F')
    header.pack(fill="x")
    image_label = ctk.CTkLabel(header, image=ctk_image, text="")
    image_label.place(x=50,y=0)
    ctk.CTkLabel(header, text="WELCOME TO THE GRADE BOT MANAGER", font=('Arial', 20, 'bold'),text_color="white").place(x=150,y=10)

    ctk.CTkLabel(login, text="Username:", font=('Arial', 12)).place(x=80, y=70)
    entry_user = ctk.CTkEntry(login, width=300)
    entry_user.place(x=200, y=70)

    ctk.CTkLabel(login, text="Password:", font=('Arial', 12)).place(x=80, y=140)
    entry_password = ctk.CTkEntry(login, show="*", width=300)
    entry_password.place(x=200, y=140)

    ctk.CTkButton(login, text="Login", command=login_attempt,width=100).place(x=200, y=250)
    ctk.CTkButton(login, text="Sign up", command=lambda: [login.destroy(), Sign_up.open_signup()],width=100).place(x=380, y=250)

    login.mainloop()

if __name__ == "__main__":
    logging_in()