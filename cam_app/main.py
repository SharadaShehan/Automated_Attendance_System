import tkinter as tk
from tkinter import ttk

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tkinter Navigation App")
        self.width = 800
        self.height = 600
        self.geometry(f"{self.width}x{self.height}")

        style = ttk.Style()
        style.layout('TNotebook.Tab', [])  # turn off tabs
        style.configure('Custom.TButton', font=('Helvetica', 12))  # Set the font size here

        self.notebook = ttk.Notebook(self)
        self.notebook.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        # self.notebook.configure(width=int(self.width * 0.8), height=int(self.height * 0.8))

        self.runAppPage = RunAppPage(self.notebook, self)
        self.registerUserPage = RegisterUserPage(self.notebook, self)
        self.homePage = HomePage(self.notebook, self)
        self.onBoarding = OnBoarding(self.notebook, self)

        self.notebook.add(self.onBoarding, text="OnBoarding")
        self.notebook.add(self.homePage, text="Home")
        self.notebook.add(self.runAppPage, text="Run App")
        self.notebook.add(self.registerUserPage, text="Register User")

        self.notebook.select(1)

class OnBoarding(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="OnBoarding Page Content", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Go to Page One", command=lambda: controller.notebook.select(1))
        button.pack(pady=10)

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

class RunAppPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="App is running...", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Exit", style='Custom.TButton', command=lambda: controller.notebook.select(1))
        button.pack(pady=10)

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

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
