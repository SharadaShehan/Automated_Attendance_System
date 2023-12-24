import tkinter as tk
from tkinter import ttk
from .HomeComponent import HomePage
from .LoginComponent import LoginPage
from .OnBoardingComponent import OnBoardingPage
from .RegisterUserComponent import RegisterUserPage
from .RunComponent import RunPage
from functions import JSONConfig

class UIApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cam App")
        self.width = 800
        self.height = 650
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

        # try:
        #     company_name = JSONConfig.read_company_name()
        #     if company_name == None:
        #         self.notebook.select(0)
        #     else:
        #         self.notebook.select(1)
        # except:
        #     self.notebook.select(0)

        self.notebook.select(3)

