import tkinter as tk
from tkinter import ttk


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # self.configure(bg="blue")

        label = tk.Label(self, text="AttendSense", font=("Helvetica", 20))
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Run App", style='Custom.TButton', command=lambda: controller.notebook.select(2))
        button.pack(pady=10)

        button = ttk.Button(self, text="Register User", style='Custom.TButton', command=lambda: controller.notebook.select(3))
        button.pack(pady=10)