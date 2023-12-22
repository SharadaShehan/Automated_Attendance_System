import tkinter as tk
from tkinter import ttk

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Login Page Content", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Go to Page One", command=lambda: controller.notebook.select(1))
        button.pack(pady=10)

