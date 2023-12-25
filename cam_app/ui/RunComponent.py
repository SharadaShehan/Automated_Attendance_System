import tkinter as tk
from tkinter import ttk
import cv2, requests
from functions import ConfigRead, Tokens
from threading import Thread
import time


class EntranceCameraThread(Thread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        cap = cv2.VideoCapture(int(self.parent.config_dict['CAMERAS']['enter_camera']))

        BaseURL = self.parent.config_dict['BACKEND']['base_url']
        URL = BaseURL + '/feed-snapshot'

        access_token = Tokens.get_access_token()
        headers = {
            "Authorization": access_token
        }

        desired_width = int(self.parent.config_dict['CAPTURE']['frame_width'])
        desired_height = int(self.parent.config_dict['CAPTURE']['frame_height'])

        while self.parent.entrance_thread_state.get():
            ret, frame = cap.read()

            if ret:
                scaled_down_frame = cv2.resize(frame, (desired_width, desired_height))
                color_corrected_frame = cv2.cvtColor(scaled_down_frame, cv2.COLOR_BGR2RGB)

                data = {
                    'photo': color_corrected_frame.tolist(),
                    'entrance': 1
                }

                try:
                    response = requests.post(URL, json=data, headers=headers)
                except requests.exceptions.ConnectionError:
                    self.parent.show_error_message("Connection Error")
                    break

                if response.status_code != 200:
                    print(response.json())
                    break
                print("entrance update successful")
                print(response.json())

                time.sleep(1)

        cap.release()
        self.parent.entrance_state_label.config(text="Stopped")
        self.parent.entrance_button.config(text="Start")
        self.parent.entrance_thread_state.set(False)


class ExitCameraThread(Thread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        cap = cv2.VideoCapture(int(self.parent.config_dict['CAMERAS']['exit_camera']))

        BaseURL = self.parent.config_dict['BACKEND']['base_url']
        URL = BaseURL + '/feed-snapshot'

        access_token = Tokens.get_access_token()
        headers = {
            "Authorization": access_token
        }

        desired_width = int(self.parent.config_dict['CAPTURE']['frame_width'])
        desired_height = int(self.parent.config_dict['CAPTURE']['frame_height'])

        while self.parent.exit_thread_state.get():
            ret, frame = cap.read()

            if ret:
                scaled_down_frame = cv2.resize(frame, (desired_width, desired_height))
                color_corrected_frame = cv2.cvtColor(scaled_down_frame, cv2.COLOR_BGR2RGB)

                data = {
                    'photo': color_corrected_frame.tolist(),
                    'entrance': 0
                }

                try:
                    response = requests.post(URL, json=data, headers=headers)
                except requests.exceptions.ConnectionError:
                    self.parent.show_error_message("Connection Error")
                    break

                if response.status_code != 200:
                    print(response.json())
                    break
                print("leave update successful")
                print(response.json())

                time.sleep(1)

        cap.release()
        self.parent.exit_state_label.config(text="Stopped")
        self.parent.exit_button.config(text="Start")
        self.parent.exit_thread_state.set(False)

class SpeechThread(Thread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        while self.parent.speech_thread_state.get():
            # ret, frame = self.controller.exit_camera.read()
            # if ret:
            #     cv2.imshow("Exit Camera", frame)
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #         break
            time.sleep(1)
            print("Speech Thread Running")
        print("Speech Thread Stopped")
        # self.controller.exit_camera.release()
        # cv2.destroyAllWindows()

class RunPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # self.start_entrance_camera()
        # self.list_camera_devices()
        self.config_dict = ConfigRead.read_config()

        self.entrance_thread_state = tk.BooleanVar()
        self.entrance_thread_state.set(False)
        self.entrance_thread = None
        self.entrance_camera_index = self.config_dict['CAMERAS']['enter_camera']

        self.exit_thread_state = tk.BooleanVar()
        self.exit_thread_state.set(False)
        self.exit_thread = None
        self.exit_camera_index = self.config_dict['CAMERAS']['exit_camera']

        self.speech_thread_state = tk.BooleanVar()
        self.speech_thread_state.set(False)
        self.speech_thread = None

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP, expand=True)

        self.middle_frame = tk.Frame(self)
        self.middle_frame.pack(side=tk.TOP, expand=True)

        # entrance camera

        self.middle_entrance_frame = tk.Frame(self.middle_frame)
        self.middle_entrance_frame.pack(side=tk.TOP, expand=True)

        self.entrance_title_label = tk.Label(self.middle_entrance_frame, text="Entrance Camera", font=("Helvetica", 12))
        self.entrance_title_label.pack(padx=10, pady=10, side=tk.LEFT)

        self.entrance_state_label = tk.Label(self.middle_entrance_frame, text="Stopped", font=("Helvetica", 12))
        self.entrance_state_label.pack(padx=10, pady=10, side=tk.LEFT)

        self.entrance_button = ttk.Button(self.middle_entrance_frame, text="Start", command=self.toggle_entrance_thread)
        self.entrance_button.pack(padx=10, pady=10, side=tk.LEFT)

        # exit camera

        self.middle_exit_frame = tk.Frame(self.middle_frame)
        self.middle_exit_frame.pack(side=tk.TOP, expand=True)

        self.exit_title_label = tk.Label(self.middle_exit_frame, text="Exit Camera", font=("Helvetica", 12))
        self.exit_title_label.pack(padx=10, pady=10, side=tk.LEFT)

        self.exit_state_label = tk.Label(self.middle_exit_frame, text="Stopped", font=("Helvetica", 12))
        self.exit_state_label.pack(padx=10, pady=10, side=tk.LEFT)

        self.exit_button = ttk.Button(self.middle_exit_frame, text="Start", command=self.toggle_exit_thread)
        self.exit_button.pack(padx=10, pady=10, side=tk.LEFT)

        # speech

        self.middle_speech_frame = tk.Frame(self.middle_frame)
        self.middle_speech_frame.pack(side=tk.TOP, expand=True)

        self.speech_title_label = tk.Label(self.middle_speech_frame, text="Speech", font=("Helvetica", 12))
        self.speech_title_label.pack(padx=10, pady=10, side=tk.LEFT)

        self.speech_state_label = tk.Label(self.middle_speech_frame, text="Stopped", font=("Helvetica", 12))
        self.speech_state_label.pack(padx=10, pady=10, side=tk.LEFT)

        self.speech_button = ttk.Button(self.middle_speech_frame, text="Start", command=self.toggle_speech_thread)
        self.speech_button.pack(padx=10, pady=10, side=tk.LEFT)

        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(side=tk.TOP, expand=True)

        button = ttk.Button(self.bottom_frame, text="Exit", style='Custom.TButton', command=self.exit_page)
        button.pack(pady=10)

    def toggle_entrance_thread(self):
        if self.entrance_thread_state.get():
            self.entrance_thread_state.set(False)
            self.entrance_state_label.config(text="Stopped")
            self.entrance_button.config(text="Start")
        else:
            self.entrance_thread_state.set(True)
            self.entrance_state_label.config(text="Running")
            self.entrance_button.config(text="Stop")
            EntranceCameraThread(self).start()

    def toggle_exit_thread(self):
        if self.exit_thread_state.get():
            self.exit_thread_state.set(False)
            self.exit_state_label.config(text="Stopped")
            self.exit_button.config(text="Start")
        else:
            self.exit_thread_state.set(True)
            self.exit_state_label.config(text="Running")
            self.exit_button.config(text="Stop")
            ExitCameraThread(self).start()

    def toggle_speech_thread(self):
        if self.speech_thread_state.get():
            self.speech_thread_state.set(False)
            self.speech_state_label.config(text="Stopped")
            self.speech_button.config(text="Start")
        else:
            self.speech_thread_state.set(True)
            self.speech_state_label.config(text="Running")
            self.speech_button.config(text="Stop")
            SpeechThread(self).start()

    def exit_page(self):
        if self.entrance_thread_state.get():
            self.entrance_thread_state.set(False)
            self.entrance_state_label.config(text="Stopped")
            self.entrance_button.config(text="Start")
        if self.exit_thread_state.get():
            self.exit_thread_state.set(False)
            self.exit_state_label.config(text="Stopped")
            self.exit_button.config(text="Start")
        if self.speech_thread_state.get():
            self.speech_thread_state.set(False)
            self.speech_state_label.config(text="Stopped")
            self.speech_button.config(text="Start")
        self.controller.notebook.select(2)

    def show_error_message(self, message):
        error_message = tk.Toplevel(self)
        error_message.title("Error")
        label = tk.Label(error_message, text=message, font=("Helvetica", 12))
        label.pack(padx=10, pady=10)
        ok_button = ttk.Button(error_message, text="OK", command=error_message.destroy)
        ok_button.pack(pady=10)

