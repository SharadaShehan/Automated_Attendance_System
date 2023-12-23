import tkinter as tk
from tkinter import ttk
import re, cv2
from PIL import Image, ImageTk

class OnBoardingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.photo = None

        # Create topand bottom frames
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP, padx=10, pady=5)

        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(side=tk.TOP, padx=10, pady=5)

        # Create left and right subframes
        self.left_frame = tk.Frame(self.top_frame)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=5)

        self.right_frame = tk.Frame(self.top_frame)
        self.right_frame.pack(side=tk.LEFT, padx=10, pady=5)

        # Create bottom subframes
        self.bottom_top_frame = tk.Frame(self.bottom_frame)
        self.bottom_top_frame.pack(side=tk.TOP)

        self.bottom_bottom_frame = tk.Frame(self.bottom_frame)
        self.bottom_bottom_frame.pack(side=tk.TOP)

        # Register Company

        label = tk.Label(self.left_frame, text="Register Company", font=("Helvetica", 14))
        label.pack(pady=(10, 10), padx=10)

        label = tk.Label(self.left_frame, text="Company Name :", font=("Helvetica", 12))
        label.pack(pady=(10, 5), padx=10)

        self.company_name_entry = tk.Entry(self.left_frame, width=30, font=("Helvetica", 14))
        self.company_name_entry.pack(padx=20)

        label = tk.Label(self.left_frame, text="Cam App Login Credentials", font=("Helvetica", 14))
        label.pack(pady=(15, 0), padx=10)

        label = tk.Label(self.left_frame, text="Username :", font=("Helvetica", 12))
        label.pack(pady=(10, 5), padx=10)

        self.username_entry = tk.Entry(self.left_frame, width=30, font=("Helvetica", 14))
        self.username_entry.pack(padx=20)

        label = tk.Label(self.left_frame, text="Password :", font=("Helvetica", 12))
        label.pack(pady=(10, 5), padx=10)

        self.password_entry = tk.Entry(self.left_frame, width=30, font=("Helvetica", 14), show="*")
        self.password_entry.pack(padx=20)

        # Register Default Executive User

        label = tk.Label(self.right_frame, text="Register Default Executive User", font=("Helvetica", 14))
        label.pack(pady=(10, 10), padx=10)

        ttk.Label(self.right_frame, text="Email :", font=("Helvetica", 12)).pack(padx=(5, 5), pady=(10, 5))
        self.email_entry = ttk.Entry(self.right_frame, width=30, font=("Helvetica", 12))
        self.email_entry.pack(padx=20)

        ttk.Label(self.right_frame, text="Password :", font=("Helvetica", 12)).pack(padx=(5, 5), pady=(10, 5))
        self.password_entry = ttk.Entry(self.right_frame, width=30, font=("Helvetica", 12), show="*")
        self.password_entry.pack(padx=20)

        ttk.Label(self.right_frame, text="First Name :", font=("Helvetica", 12)).pack(padx=(5, 5), pady=(10, 5))
        self.first_name_entry = ttk.Entry(self.right_frame, width=30, font=("Helvetica", 12))
        self.first_name_entry.pack(padx=20)

        ttk.Label(self.right_frame, text="Last Name :", font=("Helvetica", 12)).pack(padx=(5, 5), pady=(10, 5))
        self.last_name_entry = ttk.Entry(self.right_frame, width=30, font=("Helvetica", 12))
        self.last_name_entry.pack(padx=20)

        self.bottom_top_right_frame = tk.Frame(self.bottom_top_frame)
        self.bottom_top_right_frame.pack(side=tk.RIGHT)

        ttk.Label(self.bottom_top_right_frame, text="Executive User Photo :", font=("Helvetica", 12)).pack(padx=(5, 5), side=tk.LEFT)

        self.photo_label = ttk.Label(self.bottom_top_right_frame)
        self.photo_label.pack(padx=(5, 5), pady=(0, 10), side=tk.LEFT)

        ttk.Button(self.bottom_top_right_frame, text="Snap Photo", style='Custom.TButton', command=self.snap_photo).pack(padx=(5, 5),
                                                                                                  pady=(0, 10), side=tk.LEFT)


        label = tk.Label(self.bottom_bottom_frame, text="Already Registered ?", font=("Helvetica", 12))
        label.pack(side=tk.LEFT, padx=(40, 5))

        button = ttk.Button(self.bottom_bottom_frame, text="Go to Login", command=lambda: self.controller.notebook.select(1),
                            style='Custom.TButton')
        button.pack(side=tk.LEFT, padx=(5, 20))

        button = ttk.Button(self.bottom_bottom_frame, text="Cancel", style='Custom.TButton', command=lambda: controller.notebook.select(1))
        button.pack(side=tk.LEFT, padx=(70, 5))

        button = ttk.Button(self.bottom_bottom_frame, text="Register", style='Custom.TButton', command=self.register_company)
        button.pack(side=tk.LEFT, padx=(0, 10))

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

    def show_error_message(self, message):
        error_message = tk.Toplevel(self)
        error_message.title("Error")
        label = tk.Label(error_message, text=message, font=("Helvetica", 12))
        label.pack(padx=10, pady=10)
        ok_button = ttk.Button(error_message, text="OK", command=error_message.destroy)
        ok_button.pack(pady=10)

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
        if photo is None:
            return False
        # Add your photo validation regex here
        return True

    def check_user_validity(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        photo = self.photo

        if not self.validate_email(email):
            self.show_error_message("Invalid email address!")
            return False

        if not self.validate_password(password):
            self.show_error_message("Invalid password!")
            return False

        if not self.validate_name(first_name):
            self.show_error_message("Invalid first name!")
            return False

        if not self.validate_name(last_name):
            self.show_error_message("Invalid last name!")
            return False

        if not self.validate_photo(photo):
            self.show_error_message("Invalid photo!")
            return False

        return True

    def validate_company_name(self, company_name):
        # Add your company name validation regex here
        return re.match(r'^[a-zA-Z0-9\s]{1,30}$', company_name)

    def validate_cam_app_username(self, username):
        # Add your username validation regex here
        return re.match(r'^[a-zA-Z0-9_]{4,30}$', username)

    def validate_cam_app_password(self, password):
        # Add your password validation regex here
        return re.match(r'^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,30}$', password)

    def register_company(self):
        company_name = self.company_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate inputs
        if not self.validate_company_name(company_name):
            self.show_error_message("""Invalid company name.
            Use only letters, numbers, and spaces.""")
            return

        if not self.validate_cam_app_username(username):
            self.show_error_message("""Invalid username.
            Username should be at least 4 characters long and
            contain only letters, numbers, and underscores.""")
            return

        if not self.validate_cam_app_password(password):
            self.show_error_message("""Invalid password. 
            Password should be at least 8 characters long and 
            contain at least one number and one special character.""")
            return

        if not self.check_user_validity():
            return

        # Now you can use the values as needed
        print("Registering Company...")
        print("Company Name:", company_name)
        print("Username:", username)
        print("Password:", password)

        # Example: Change to the next page in the notebook
        self.controller.notebook.select(1)
