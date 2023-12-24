import tkinter as tk
from tkinter import ttk
import cv2, requests
from functions import JSONConfig

class RunPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # self.start_entrance_camera()

        label = tk.Label(self, text="App is running...", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Exit", style='Custom.TButton', command=lambda: controller.notebook.select(1))
        button.pack(pady=10)

    def show_error_message(self, message):
        error_message = tk.Toplevel(self)
        error_message.title("Error")
        label = tk.Label(error_message, text=message, font=("Helvetica", 12))
        label.pack(padx=10, pady=10)
        ok_button = ttk.Button(error_message, text="OK", command=error_message.destroy)
        ok_button.pack(pady=10)

    def start_entrance_camera(self, camera_index=0):
        cap = cv2.VideoCapture(camera_index)

        BaseURL = JSONConfig.read_url()
        URL = BaseURL + '/feed-snapshot'

        access_token = JSONConfig.read_access_token()
        headers = {
            "Authorization": access_token
        }

        while True:
            ret, frame = cap.read()

            if ret:
                desired_width = 200
                desired_height = 150
                scaled_down_frame = cv2.resize(frame, (desired_width, desired_height))
                color_corrected_frame = cv2.cvtColor(scaled_down_frame, cv2.COLOR_BGR2RGB)

                data = {
                    'photo': color_corrected_frame.tolist(),
                    'entrance': 1
                }

                response = requests.post(URL, json=data, headers=headers)
                if response.status_code != 200:
                    # self.show_error_message(response.json()['message'])
                    print(response.json())
                    break
                print("successful")
                print(response.json())

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            break

        cap.release()
        # cv2.destroyAllWindows()

        self.controller.notebook.select(2)
