import queue
from database.models import CustomUser
from middleware_api.ml_model_src.functions import liveness_checker
import face_recognition
import numpy as np
import datetime, os, json
import paho.mqtt.client as paho

class MLModel:
    pending_tasks = queue.Queue(maxsize=20)
    mqtt_client = paho.Client()
    users_data = []

    @classmethod
    def start_ml_model(cls):
        current_directory = os.path.dirname(__file__)
        liveness_model_dir = os.path.join(current_directory, "ml_model_src\\resources\\anti_spoof_models")
        users_data = CustomUser.objects.all().values('id', 'encodings',)
        cls.users_data = [{'id': user_data['id'],
                           'encodings': np.array(json.loads(user_data['encodings']))} for user_data in users_data]

        while True:
            if not cls.pending_tasks.empty():
                # Get the next pending process
                task_data = cls.pending_tasks.get()
                list_image = task_data['photo']
                entrance = int(task_data['entrance'])
                converted_image = np.array(list_image).astype(np.uint8)
                liveness, value = liveness_checker.test(image=converted_image, model_dir=liveness_model_dir, device_id=0)

                if liveness == 1:
                    try:
                        encoded_image = face_recognition.face_encodings(converted_image)[0]
                    except IndexError:
                        continue
                    distance_list = []
                    for user_data in cls.users_data:
                        user_encodings = user_data['encodings']
                        distance = face_recognition.face_distance([user_encodings], encoded_image)
                        distance_list.append(distance)
                    min_distance = min(distance_list)
                    if min_distance < 0.5:
                        detected_user_data = cls.users_data[distance_list.index(min_distance)]
                        detected_user = CustomUser.objects.get(id=detected_user_data['id'])

                        attendance_obj = json.loads(detected_user.attendance)

                        x = datetime.datetime.now()
                        date, time = x.strftime("%Y-%m-%d %H-%M").split()
                        date_strings_list = date.split("-")

                        if date_strings_list[0] in attendance_obj:
                            if date_strings_list[1] in attendance_obj[date_strings_list[0]]:
                                if date_strings_list[2] in attendance_obj[date_strings_list[0]][date_strings_list[1]]:
                                    pass
                                else:
                                    attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]] = {'entrance': [], 'leave': []}
                            else:
                                attendance_obj[date_strings_list[0]][date_strings_list[1]] = {date_strings_list[2]: {'entrance': [], 'leave': []}}
                        else:
                            attendance_obj[date_strings_list[0]] = {date_strings_list[1]: {date_strings_list[2]: {'entrance': [], 'leave': []}}}

                        if entrance == 1:
                            attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['entrance'].append(time)
                        elif entrance == 0:
                            attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['leave'].append(time)

                        detected_user.attendance = json.dumps(attendance_obj)
                        detected_user.save()

                        greeting = 'Welcome' if entrance == 1 else 'Goodbye'
                        signature = 'Mr.' if detected_user.gender == 'Male' else 'Ms.'
                        user_name = detected_user.first_name + ' ' + detected_user.last_name
                        greeting = greeting + ' ' + signature + ' ' + user_name
                        if cls.mqtt_client.connect('localhost', 1883) == 0:
                            cls.mqtt_client.publish('attendance', greeting)
                            cls.mqtt_client.disconnect()
                        else:
                            raise Exception('MQTT Connection Error')

    @classmethod
    def add_task(cls, input_data):
        if not cls.pending_tasks.full():
            cls.pending_tasks.put(input_data)
            return True
        return False

    # @classmethod
    # def get_result(cls):
    #     if not cls.finished_tasks.empty():
    #         return cls.finished_tasks.get()
    #     return None

    @classmethod
    def add_user_encodings(cls, user_data):
        cls.users_data.append(user_data)
        return True
