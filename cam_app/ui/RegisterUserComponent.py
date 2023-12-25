import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import re, requests
from functions import ConfigRead, Tokens


class RegisterUserPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.photo = None

        label = tk.Label(self, text="Register User", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        ttk.Label(self, text="Email :", font=("Helvetica", 12)).pack(padx=(5, 5), pady=(0, 3))
        self.email_entry = ttk.Entry(self, width=30, font=("Helvetica", 12))
        self.email_entry.pack(padx=(5, 5), pady=(0, 10))

        ttk.Label(self, text="Password :", font=("Helvetica", 12)).pack(padx=(5, 5), pady=(0, 3))
        self.password_entry = ttk.Entry(self, width=30, font=("Helvetica", 12), show="*")
        self.password_entry.pack(padx=(5, 5), pady=(0, 10))

        ttk.Label(self, text="First Name :", font=("Helvetica", 12)).pack(padx=(5, 5), pady=(0, 3))
        self.first_name_entry = ttk.Entry(self, width=30, font=("Helvetica", 12))
        self.first_name_entry.pack(padx=(5, 5), pady=(0, 10))

        ttk.Label(self, text="Last Name :", font=("Helvetica", 12)).pack(padx=(5, 5), pady=(0, 3))
        self.last_name_entry = ttk.Entry(self, width=30, font=("Helvetica", 12))
        self.last_name_entry.pack(padx=(5, 5), pady=(0, 10))

        self.radio_var = tk.StringVar()
        self.radio_var.set("Option 1")

        self.gender_frame = tk.Frame(self)
        self.gender_frame.pack(padx=(5, 5), pady=(0, 10))

        ttk.Label(self.gender_frame, text="Gender :", font=("Helvetica", 12)).pack(padx=(30, 5), side=tk.LEFT)

        radio_button1 = tk.Radiobutton(self.gender_frame, text="Male", variable=self.radio_var, value="Male",
                                       font=("Helvetica", 12))
        radio_button1.pack(side=tk.LEFT, padx=(5, 5))

        radio_button2 = tk.Radiobutton(self.gender_frame, text="Female", variable=self.radio_var, value="Female",
                                       font=("Helvetica", 12))
        radio_button2.pack(side=tk.LEFT, padx=(5, 5))

        ttk.Label(self, text="Photo :", font=("Helvetica", 12)).pack(padx=(5, 5))

        self.photo_label = ttk.Label(self)
        self.photo_label.pack(padx=(5, 5), pady=(0, 10))

        ttk.Button(self, text="Snap Photo", style='Custom.TButton', command=self.snap_photo).pack(padx=(5, 5), pady=(0, 10))

        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(padx=(5, 5), pady=(10, 10))

        button = ttk.Button(self.bottom_frame, text="Cancel", style='Custom.TButton', command=lambda: controller.notebook.select(1))
        button.pack(side=tk.LEFT, padx=(5, 5))

        button = ttk.Button(self.bottom_frame, text="Register", style='Custom.TButton', command=self.register_user)
        button.pack(side=tk.LEFT, padx=(5, 5))

        # if not ConfigRead.check_config_initialized():
        #     self.controller.notebook.select(5)
        # elif not ConfigRead.check_company_initialized():
        #     self.controller.notebook.select(0)

    def validate_email(self, email):
        # Add email validation regex here
        return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

    def validate_password(self, password):
        # Add your password validation regex here
        return re.match(r'^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,30}$', password)

    def validate_name(self, name):
        # Add your name validation regex here
        return re.match(r'^[a-zA-Z]+$', name)

    def validate_gender(self, gender):
        return True if gender in ["Male", "Female"] else False

    def validate_photo(self, photo):
        if photo is None:
            return False
        # Add your photo validation regex here
        return True

    def show_error_message(self, message):
        error_message = tk.Toplevel(self)
        error_message.title("Error")
        label = tk.Label(error_message, text=message, font=("Helvetica", 12))
        label.pack(padx=10, pady=10)
        ok_button = ttk.Button(error_message, text="OK", command=error_message.destroy)
        ok_button.pack(pady=10)

    def snap_photo(self):
        config_dict = ConfigRead.read_config()
        camera_index = int(config_dict['CAMERAS']['registration_camera'])
        cap = cv2.VideoCapture(camera_index)
        ret, frame = cap.read()
        cap.release()

        desired_width = int(config_dict['CAPTURE']['frame_width'])
        desired_height = int(config_dict['CAPTURE']['frame_height'])
        scaled_down_frame = cv2.resize(frame, (desired_width, desired_height))
        color_corrected_frame = cv2.cvtColor(scaled_down_frame, cv2.COLOR_BGR2RGB)

        self.photo = color_corrected_frame

        # Convert the OpenCV frame to a format compatible with Tkinter
        pil_image = Image.fromarray(color_corrected_frame)

        # Convert the resized image to a PhotoImage
        photo = ImageTk.PhotoImage(pil_image)

        # Update the label with the new photo
        self.photo_label.configure(image=photo)
        self.photo_label.image = photo  # Keep a reference to prevent garbage collection

    def register_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        gender = self.radio_var.get()
        photo = self.photo

        if not self.validate_email(email):
            self.show_error_message("Invalid email address!")
            return

        if not self.validate_password(password):
            self.show_error_message("Invalid password!")
            return

        if not self.validate_name(first_name):
            self.show_error_message("Invalid first name!")
            return

        if not self.validate_name(last_name):
            self.show_error_message("Invalid last name!")
            return

        if not self.validate_gender(gender):
            self.show_error_message("Gender not selected!")
            return

        if not self.validate_photo(photo):
            self.show_error_message("Invalid photo!")
            return

        BaseURL = ConfigRead.read_config()['BACKEND']['base_url']
        URL = BaseURL + "/create/user"

        init_token = Tokens.get_init_token()

        data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "photo": photo.tolist()
        }
        headers = {
            "Authorization": init_token
        }

        try:
            response = requests.post(URL, json=data, headers=headers)
        except requests.exceptions.ConnectionError:
            self.show_error_message("Error connecting to server!")
            return

        if response.status_code != 201:
            self.show_error_message(f"Error registering user :{response.json()['message']}")
            return

        self.show_error_message("User registered successfully!")
        self.controller.notebook.select(2)
