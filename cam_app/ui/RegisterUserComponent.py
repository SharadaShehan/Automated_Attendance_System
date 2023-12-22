import tkinter as tk
from tkinter import ttk

class RegisterUserPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Register User", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        ttk.Label(self, text="Last name :").pack(anchor=tk.W)
        ttk.Label(self, text="First name :").pack(anchor=tk.W)
        ttk.Label(self, text="Password :").pack(anchor=tk.W)
        ttk.Label(self, text="Email :").pack(anchor=tk.W)
        ttk.Label(self, text="Employee Account Details :").pack(anchor=tk.W)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        ttk.Label(self, text="Department :").pack(anchor=tk.W)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        ttk.Button(self, text="Snap Photo").pack(pady=5)

        button = ttk.Button(self, text="Register", style='Custom.TButton', command=lambda: controller.notebook.select(1))
        button.pack(pady=5)

        button = ttk.Button(self, text="Cancel", style='Custom.TButton', command=lambda: controller.notebook.select(1))
        button.pack(pady=5)

        ttk.Label(self, text="Powered by AttendSense").pack(pady=5)
        ttk.Label(self, text="Register User Form", font=("TkDefaultFont", 16)).pack(pady=10)
