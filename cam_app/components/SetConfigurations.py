import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from functions import ConfigRead


class CameraSettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.camera_list = []
        self.sample_snap = None
        self.registration_camera = None
        self.enter_camera = None
        self.exit_camera = None
        self.config_dict = ConfigRead.read_config()

        for i in range(10):  # You can adjust the range based on the number of devices you expect
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if not cap.isOpened():
                break
            else:
                self.camera_list.append(
                    {
                        'index': i,
                        'text': f"Camera {i} - {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))} x {int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}"
                    }
                )
                cap.release()

        label = tk.Label(self, text="Camera Configuration", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        self.frame_top = tk.Frame(self)
        self.frame_top.pack(side=tk.TOP, pady=10, padx=10)

        self.frame_top_top = tk.Frame(self.frame_top)
        self.frame_top_top.pack(side=tk.TOP, pady=5, padx=10)

        label = tk.Label(self.frame_top_top, text="Registration Camera ", font=("Helvetica", 12))
        label.pack(pady=5, padx=10, side=tk.LEFT)

        self.registration_camera = ttk.Combobox(self.frame_top_top,
            values=[camera['text'].split()[0]+" "+camera['text'].split()[1] for camera in self.camera_list], state="readonly")
        self.registration_camera.pack(pady=5, padx=10, side=tk.LEFT)

        self.frame_top_middle = tk.Frame(self.frame_top)
        self.frame_top_middle.pack(side=tk.TOP, pady=5, padx=10)

        label = tk.Label(self.frame_top_middle, text="Entrance Camera ", font=("Helvetica", 12))
        label.pack(pady=5, padx=10, side=tk.LEFT)

        self.enter_camera = ttk.Combobox(self.frame_top_middle,
            values=[camera['text'].split()[0]+" "+camera['text'].split()[1] for camera in self.camera_list], state="readonly")
        self.enter_camera.pack(pady=5, padx=10, side=tk.LEFT)

        self.frame_top_bottom = tk.Frame(self.frame_top)
        self.frame_top_bottom.pack(side=tk.TOP, pady=5, padx=10)

        label = tk.Label(self.frame_top_bottom, text="Exit Camera ", font=("Helvetica", 12))
        label.pack(pady=5, padx=10, side=tk.LEFT)

        self.exit_camera = ttk.Combobox(self.frame_top_bottom,
            values=[camera['text'].split()[0]+" "+camera['text'].split()[1] for camera in self.camera_list], state="readonly")
        self.exit_camera.pack(pady=5, padx=10, side=tk.LEFT)

        self.frame_top_bottom_buttons = tk.Frame(self.frame_top)
        self.frame_top_bottom_buttons.pack(side=tk.TOP, pady=10, padx=10)

        button = ttk.Button(self.frame_top_bottom_buttons, text="Cancel", style='Custom.TButton', command=lambda: controller.notebook.select(2))
        button.pack(pady=10, padx=10, side=tk.LEFT)

        button = ttk.Button(self.frame_top_bottom_buttons, text="Save", style='Custom.TButton', command=self.save_configurations)
        button.pack(pady=10, padx=10, side=tk.LEFT)

        self.frame_bottom = tk.Frame(self)
        self.frame_bottom.pack(side=tk.BOTTOM, pady=5, padx=10)

        self.frame_bottom_left = tk.Frame(self.frame_bottom)
        self.frame_bottom_left.pack(side=tk.LEFT, pady=0, padx=10)

        self.frame_bottom_right = tk.Frame(self.frame_bottom)
        self.frame_bottom_right.pack(side=tk.RIGHT, pady=0, padx=10)

        for camera in self.camera_list:
            self.mini_frame = tk.Frame(self.frame_bottom_left)
            self.mini_frame.pack(pady=2, padx=10)
            label = tk.Label(self.mini_frame, text=camera['text'], font=("Helvetica", 10))
            label.pack(pady=0, padx=10, side=tk.LEFT)
            snap_button = ttk.Button(self.mini_frame, text="Test", command=lambda: self.snap_camera(camera['index']))
            snap_button.pack(pady=0, padx=10, side=tk.LEFT)

        self.sample_snap = ttk.Label(self.frame_bottom_right)
        self.sample_snap.pack(pady=10, padx=10)

        # if ConfigRead.check_company_initialized():
        #     self.controller.notebook.select(1)
        # elif ConfigRead.check_config_initialized():
        #     self.controller.notebook.select(0)

    def show_error_message(self, message):
        error_message = tk.Toplevel(self)
        error_message.title("Error")
        label = tk.Label(error_message, text=message, font=("Helvetica", 12))
        label.pack(padx=10, pady=10)
        ok_button = ttk.Button(error_message, text="OK", command=error_message.destroy)
        ok_button.pack(pady=10)

    def snap_camera(self, camera_index=0):
        cap = cv2.VideoCapture(camera_index)
        ret, frame = cap.read()
        cap.release()

        desired_width = int(self.config_dict['CAPTURE']['frame_width'])
        desired_height = int(self.config_dict['CAPTURE']['frame_height'])

        scaled_down_frame = cv2.resize(frame, (desired_width, desired_height))
        color_corrected_frame = cv2.cvtColor(scaled_down_frame, cv2.COLOR_BGR2RGB)
        # Convert the OpenCV frame to a format compatible with Tkinter
        pil_image = Image.fromarray(color_corrected_frame)

        # Convert the resized image to a PhotoImage
        sample_image = ImageTk.PhotoImage(pil_image)

        self.sample_snap.configure(image=sample_image)
        self.sample_snap.image = sample_image

        # cv2.destroyAllWindows()

    def save_configurations(self):
        registration_camera = self.registration_camera.get()
        enter_camera = self.enter_camera.get()
        exit_camera = self.exit_camera.get()

        if not registration_camera or not enter_camera or not exit_camera:
            self.show_error_message("Please select cameras for all the options.")
            return

        if enter_camera == exit_camera:
            self.show_error_message("Please select different cameras for entrance and exit.")
            return

        registration_camera_index = int(registration_camera.split()[1])
        enter_camera_index = int(enter_camera.split()[1])
        exit_camera_index = int(exit_camera.split()[1])

        if ConfigRead.check_company_initialized():
            status = ConfigRead.update_camera_config(registration_camera_index, enter_camera_index, exit_camera_index)
            if status:
                self.controller.notebook.select(2)
            else:
                self.show_error_message("Error saving configurations. Please try again.")
        else:
            status = ConfigRead.create_config(registration_camera_index, enter_camera_index, exit_camera_index)
            if status:
                self.controller.notebook.select(0)
            else:
                self.show_error_message("Error saving configurations. Please try again.")

