import tkinter as tk
from tkinter import ttk
import re

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Cam App Login", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        label = tk.Label(self, text="Email :", font=("Helvetica", 12))
        label.pack(pady=(2, 0), padx=10)

        self.email_entry = tk.Entry(self, width=30, font=("Helvetica", 14))
        self.email_entry.pack(pady=10, padx=20)

        label = tk.Label(self, text="Password :", font=("Helvetica", 12))
        label.pack(pady=(2, 0), padx=10)

        self.password_entry = tk.Entry(self, width=30, font=("Helvetica", 14), show="*")
        self.password_entry.pack(pady=10, padx=20)

        button = ttk.Button(self, text="login", command=self.app_login, style='Custom.TButton')
        button.pack(pady=10)

    def validate_email(self, email):
        # Add email validation regex here
        return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

    def validate_password(self, password):
        # Add your password validation regex here
        return re.match(r'^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,30}$', password)

    def show_error_message(self, message):
        error_message = tk.Toplevel(self)
        error_message.title("Error")
        label = tk.Label(error_message, text=message, font=("Helvetica", 12))
        label.pack(padx=10, pady=10)
        ok_button = ttk.Button(error_message, text="OK", command=error_message.destroy)
        ok_button.pack(pady=10)

    def app_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Validate inputs
        if not self.validate_email(email):
            self.show_error_message("Invalid email.")
            return

        if not self.validate_password(password):
            self.show_error_message("Invalid password.")
            return

        # Now you can use the values as needed
        print("Login In...")
        print("Email:", email)
        print("Password:", password)

        # Example: Change to the next page in the notebook
        self.controller.notebook.select(2)
