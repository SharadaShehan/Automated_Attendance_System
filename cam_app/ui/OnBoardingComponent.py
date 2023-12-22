import tkinter as tk
from tkinter import ttk
import re

class OnBoardingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Register Company", font=("Helvetica", 14))
        label.pack(pady=(10, 20), padx=10)

        label = tk.Label(self, text="Company Name :", font=("Helvetica", 18))
        label.pack(pady=(15, 0), padx=10)

        self.company_name_entry = tk.Entry(self, width=30, font=("Helvetica", 14))
        self.company_name_entry.pack(pady=10, padx=20)

        label = tk.Label(self, text="Cam App Login Credentials", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        label = tk.Label(self, text="Username :", font=("Helvetica", 12))
        label.pack(pady=(2, 0), padx=10)

        self.username_entry = tk.Entry(self, width=30, font=("Helvetica", 14))
        self.username_entry.pack(pady=10, padx=20)

        label = tk.Label(self, text="Password :", font=("Helvetica", 12))
        label.pack(pady=(2, 0), padx=10)

        self.password_entry = tk.Entry(self, width=30, font=("Helvetica", 14))
        self.password_entry.pack(pady=10, padx=20)

        button = ttk.Button(self, text="Register", command=self.register_company, style='Custom.TButton')
        button.pack(pady=10)

    def validate_company_name(self, company_name):
        # Add your company name validation regex here
        return re.match(r'^[a-zA-Z0-9\s]{1,30}$', company_name)

    def validate_username(self, username):
        # Add your username validation regex here
        return re.match(r'^[a-zA-Z0-9_]{4,30}$', username)

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

    def register_company(self):
        company_name = self.company_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate inputs
        if not self.validate_company_name(company_name):
            self.show_error_message("""Invalid company name.
            Use only letters, numbers, and spaces.""")
            return

        if not self.validate_username(username):
            self.show_error_message("""Invalid username.
            Username should be at least 4 characters long and
            contain only letters, numbers, and underscores.""")
            return

        if not self.validate_password(password):
            self.show_error_message("""Invalid password. 
            Password should be at least 8 characters long and 
            contain at least one number and one special character.""")
            return
        # Now you can use the values as needed
        print("Registering Company...")
        print("Company Name:", company_name)
        print("Username:", username)
        print("Password:", password)

        # Example: Change to the next page in the notebook
        self.controller.notebook.select(1)
