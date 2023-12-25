import tkinter as tk
from tkinter import ttk
import re, requests
from functions import ConfigRead, Tokens


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Cam App Login", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        label = tk.Label(self, text="Username :", font=("Helvetica", 12))
        label.pack(pady=(2, 0), padx=10)

        self.username_entry = tk.Entry(self, width=30, font=("Helvetica", 14))
        self.username_entry.pack(pady=10, padx=20)

        label = tk.Label(self, text="Password :", font=("Helvetica", 12))
        label.pack(pady=(2, 0), padx=10)

        self.password_entry = tk.Entry(self, width=30, font=("Helvetica", 14), show="*")
        self.password_entry.pack(pady=10, padx=20)

        button = ttk.Button(self, text="login", command=self.app_login, style='Custom.TButton')
        button.pack(pady=10)

        if not ConfigRead.check_config_initialized():
            self.controller.notebook.select(5)
        elif not ConfigRead.check_company_initialized():
            self.controller.notebook.select(0)

    def validate_username(self, username):
        # Add email validation regex here
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

    def app_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate inputs
        if not self.validate_username(username):
            self.show_error_message("Invalid username.")
            return

        if not self.validate_password(password):
            self.show_error_message("Invalid password.")
            return

        BaseURL = ConfigRead.read_config()['BACKEND']['base_url']
        URL = BaseURL + "/login"

        init_token = Tokens.get_init_token()

        data = {
            "username": username,
            "password": password
        }
        headers = {
            "Authorization": init_token
        }
        response = requests.post(URL, json=data, headers=headers)

        if response.status_code == 200:
            access_token = response.json()["access_token"]
            if not Tokens.save_access_token(access_token):
                self.show_error_message("Error saving access token.")
                return
            self.controller.notebook.select(2)
        else:
            self.show_error_message("Invalid Credentials.")
            return

