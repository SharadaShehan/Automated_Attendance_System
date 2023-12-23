import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import re

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

        ttk.Label(self, text="Photo :", font=("Helvetica", 12)).pack(padx=(5, 5))

        self.photo_label = ttk.Label(self)
        self.photo_label.pack(padx=(5, 5), pady=(0, 10))

        ttk.Button(self, text="Snap Photo", style='Custom.TButton', command=self.snap_photo).pack(padx=(5, 5), pady=(0, 10))

        button = ttk.Button(self, text="Cancel", style='Custom.TButton', command=lambda: controller.notebook.select(1))
        button.pack(side=tk.LEFT, padx=(70, 5))

        button = ttk.Button(self, text="Register", style='Custom.TButton', command=lambda: controller.notebook.select(1))
        button.pack(side=tk.LEFT, padx=(0, 10))

    def validate_email(self, email):
        # Add email validation regex here
        return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

    def validate_password(self, password):
        # Add your password validation regex here
        return re.match(r'^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,30}$', password)

    def validate_name(self, name):
        # Add your name validation regex here
        return re.match(r'^[a-zA-Z]+$', name)

    def validate_photo(self, photo):
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
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        self.photo = frame

        # Convert the OpenCV frame to a format compatible with Tkinter
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Resize the image to your desired dimensions (e.g., 200x150)
        resized_image = pil_image.resize((200, 150), Image.ANTIALIAS)

        # Convert the resized image to a PhotoImage
        photo = ImageTk.PhotoImage(resized_image)

        # Update the label with the new photo
        self.photo_label.configure(image=photo)
        self.photo_label.image = photo  # Keep a reference to prevent garbage collection

        print("Photo taken!")

    def register_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
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

        if not self.validate_photo(photo):
            self.show_error_message("Invalid photo!")
            return
