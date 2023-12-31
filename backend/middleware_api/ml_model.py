import queue
from database.models import CustomUser
from middleware_api.ml_model_src.functions import liveness_checker
import face_recognition
import numpy as np
import datetime, os, json
import paho.mqtt.client as paho
import environ

env = environ.Env()
environ.Env.read_env()


class MLModel:
    pending_tasks = queue.Queue(maxsize=20)
    mqtt_client = paho.Client()
    users_data = []

    @classmethod
    def start_ml_model(cls):
        mqtt_broker = env('MQTT_BROKER')
        mqtt_port = int(env('MQTT_PORT'))
        mqtt_topic = env('MQTT_TOPIC')
        min_minutes_threshold = int(env('MIN_MINUTES_THRESHOLD'))   # Minimum minutes between two entrances or two leaves for same user

        # Start the mqtt client and connect to the broker
        if cls.mqtt_client.connect(mqtt_broker, mqtt_port) != 0:
            raise Exception('Failed to connect to mqtt broker')

        current_directory = os.path.dirname(__file__)
        liveness_model_dir = os.path.join(current_directory, "ml_model_src\\resources\\anti_spoof_models")
        # Load the users data from the database
        users_data = CustomUser.objects.all().values('id', 'encodings',)
        cls.users_data = [{'id': user_data['id'],
                           'encodings': np.array(json.loads(user_data['encodings']))} for user_data in users_data]

        while True:
            if not cls.pending_tasks.empty():
                # Get the next pending process
                task_data = cls.pending_tasks.get()
                list_image = task_data['photo']
                entrance = int(task_data['entrance'])
                # Convert the image to required format
                converted_image = np.array(list_image).astype(np.uint8)
                liveness, value = liveness_checker.test(image=converted_image, model_dir=liveness_model_dir, device_id=0)

                if liveness == 1:
                    try:
                        # Get the face encodings of the image
                        encoded_image = face_recognition.face_encodings(converted_image)[0]
                    except IndexError:
                        # If no face is detected, continue to the next process
                        continue

                    distance_list = []
                    for user_data in cls.users_data:
                        user_encodings = user_data['encodings']
                        distance = face_recognition.face_distance([user_encodings], encoded_image)
                        distance_list.append(distance)
                    # Get the best match
                    min_distance = min(distance_list)
                    # Check if the best match is close enough
                    if min_distance < 0.5:
                        # Get the user data of the best match
                        detected_user_data = cls.users_data[distance_list.index(min_distance)]
                        detected_user = CustomUser.objects.get(id=detected_user_data['id'])

                        # get the attendance object of the user and convert it to a python dictionary
                        attendance_obj = json.loads(detected_user.attendance)

                        x = datetime.datetime.now()
                        date, time = x.strftime("%Y-%m-%d %H-%M").split()
                        date_strings_list = date.split("-")

                        # Check if the date is already in the attendance object unlless create it
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


                        time_format = '%H-%M'   # expected format of time
                        if entrance == 1:
                            entrance_list_of_day = attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['entrance']
                            if len(entrance_list_of_day) > 0:
                                last_entrance = datetime.datetime.strptime(entrance_list_of_day[-1], time_format)
                                current_entrance = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H-%M").split()[1], time_format)
                                # Check if the time difference between the last entrance and the current entrance is less than the minimum minutes threshold
                                if current_entrance - last_entrance < datetime.timedelta(minutes=min_minutes_threshold):
                                    continue
                            attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['entrance'].append(time)
                        elif entrance == 0:
                            leave_list_of_day = attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['leave']
                            if len(leave_list_of_day) > 0:
                                last_leave = datetime.datetime.strptime(leave_list_of_day[-1], time_format)
                                current_leave = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H-%M").split()[1], time_format)
                                # Check if the time difference between the last leave and the current leave is less than the minimum minutes threshold
                                if current_leave - last_leave < datetime.timedelta(minutes=min_minutes_threshold):
                                    continue
                            attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['leave'].append(time)

                        # If updated successfully, save the user
                        detected_user.attendance = json.dumps(attendance_obj)
                        detected_user.save()

                        # Publish the MQTT message
                        greeting = 'Welcome' if entrance == 1 else 'Goodbye'
                        signature = 'Mr.' if detected_user.gender == 'Male' else 'Ms.'
                        user_name = detected_user.first_name + ' ' + detected_user.last_name
                        greeting = greeting + ' ' + signature + ' ' + user_name
                        cls.mqtt_client.publish(mqtt_topic, greeting)

        # close the MQTT client
        cls.mqtt_client.disconnect()

    @classmethod
    def add_task(cls, input_data):
        if not cls.pending_tasks.full():
            cls.pending_tasks.put(input_data)
            return True
        return False

    @classmethod
    def add_user_encodings(cls, user_data):
        cls.users_data.append(user_data)
        return True
