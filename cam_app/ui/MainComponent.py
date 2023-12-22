import tkinter as tk
from tkinter import ttk
from .HomeComponent import HomePage
from .LoginComponent import LoginPage
from .OnBoardingComponent import OnBoardingPage
from .RegisterUserComponent import RegisterUserPage
from .RunComponent import RunPage

class UIApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cam App")
        self.width = 800
        self.height = 600
        self.geometry(f"{self.width}x{self.height}")

        style = ttk.Style()
        style.layout('TNotebook.Tab', [])  # turn off tabs
        style.configure('Custom.TButton', font=('Helvetica', 12))  # Set the font size here

        self.notebook = ttk.Notebook(self)
        self.notebook.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        # self.notebook.configure(width=int(self.width * 0.8), height=int(self.height * 0.8))

        self.runAppPage = RunPage(self.notebook, self)
        self.registerUserPage = RegisterUserPage(self.notebook, self)
        self.loginPage = LoginPage(self.notebook, self)
        self.homePage = HomePage(self.notebook, self)
        self.onBoarding = OnBoardingPage(self.notebook, self)

        self.notebook.add(self.onBoarding, text="OnBoarding")
        self.notebook.add(self.loginPage, text="Login")
        self.notebook.add(self.homePage, text="Home")
        self.notebook.add(self.runAppPage, text="Run App")
        self.notebook.add(self.registerUserPage, text="Register User")

        self.notebook.select(0)
