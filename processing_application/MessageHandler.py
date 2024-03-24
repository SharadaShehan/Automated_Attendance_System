import os, pickle, json, datetime
import numpy as np
# from ml_model_src.functions import liveness_checker
import face_recognition
from Database import get_user_data, update_user_attendance
from dotenv import load_dotenv
from MosquittoMQTT import attendance_updated_event


load_dotenv()

def callback_function(users_data, db_conn, mqtt_client, monitoringObj, ch, method, properties, body):
    """Callback function to process messages from the RabbitMQ queue."""
    try:

        monitoringObj.write_new_message_metric(1.0)
        # Decode the message
        message = pickle.loads(body)
        photo = message['photo']
        entrance = bool(int(message['entrance']))

        # Identify the user in the photo
        user_id = identify_user(photo, users_data)

        if user_id is None:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        if entrance:
            success = update_entrance(user_id, db_conn)
        else:
            success = update_leave(user_id, db_conn)

        # Publish a message to the MQTT broker
        if success:
            monitoringObj.write_attendance_updated_metric(1.0)
            attendance_updated_event(mqtt_client, db_conn, user_id, entrance)
            monitoringObj.write_mqtt_publish_metric(1.0)

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except (Exception) as error:
        monitoringObj.write_error_metric(1.0)
        print("Error while processing message:", error)
        ch.basic_nack(delivery_tag=method.delivery_tag)


def identify_user(photo, users_data):
    """Identifies the user in the photo."""
    liveness_model_dir = "ml_model_src/resources/anti_spoof_models"
    converted_image = np.array(photo).astype(np.uint8)
    # liveness, value = liveness_checker.test(image=converted_image, model_dir=liveness_model_dir, device_id=0)

    # if liveness == 1:
    if True:
        try:
            # Get the face encodings of the image
            encoded_image = face_recognition.face_encodings(converted_image)[0]
        except IndexError:
            # If no face is detected, continue to the next process
            return None

        distance_list = []
        for user_data in users_data:
            user_encodings = user_data['encodings']
            distance = face_recognition.face_distance([user_encodings], encoded_image)
            distance_list.append(distance)

        # Get the best match
        min_distance = min(distance_list)

        # Check if the best match is close enough
        if min_distance < 0.5:
            # Get the user id of the best match
            user_id = users_data[distance_list.index(min_distance)]['id']
            return user_id


def update_entrance(user_id, db_conn):
    min_minutes_threshold = int(os.getenv('MIN_MINUTES_THRESHOLD'))
    x = datetime.datetime.now()
    date, time = x.strftime("%Y-%m-%d %H-%M").split()
    date_strings_list = date.split("-")

    try:
        user_data = get_user_data(user_id, db_conn)
        if type(user_data[1]) == str:
            attendance_obj = json.loads(user_data[1])
        else:
            attendance_obj = user_data[1]

        # Check if the date is already in the attendance object unlless create it
        attendance_obj = format_attendance_object(date_strings_list, attendance_obj)
        # update the entrance times list for the current day
        time_format = '%H-%M'
        entrance_list_of_day = attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['entrance']
        if len(entrance_list_of_day) > 0:
            last_entrance = datetime.datetime.strptime(entrance_list_of_day[-1], time_format)
            current_entrance = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H-%M").split()[1], time_format)
            # Check if the time difference between the last entrance and the current entrance is less than the minimum minutes threshold
            if current_entrance - last_entrance < datetime.timedelta(minutes=min_minutes_threshold):
                return False
        attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['entrance'].append(time)
        attendance = json.dumps(attendance_obj)
        success = update_user_attendance(user_id, attendance, db_conn)
        return success

    except Exception as e:
        print(e)
        return False


def update_leave(user_id, db_conn):
    min_minutes_threshold = int(os.getenv('MIN_MINUTES_THRESHOLD'))
    x = datetime.datetime.now()
    date, time = x.strftime("%Y-%m-%d %H-%M").split()
    date_strings_list = date.split("-")

    try:
        user_data = get_user_data(user_id, db_conn)
        if type(user_data[1]) == str:
            attendance_obj = json.loads(user_data[1])
        else:
            attendance_obj = user_data[1]
        # Check if the date is already in the attendance object unlless create it
        attendance_obj = format_attendance_object(date_strings_list, attendance_obj)
        # update the leave times list for the current day
        time_format = '%H-%M'
        leave_list_of_day = attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['leave']
        if len(leave_list_of_day) > 0:
            last_leave = datetime.datetime.strptime(leave_list_of_day[-1], time_format)
            current_leave = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H-%M").split()[1],time_format)
            # Check if the time difference between the last leave and the current leave is less than the minimum minutes threshold
            if current_leave - last_leave < datetime.timedelta(minutes=min_minutes_threshold):
                return False
        attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['leave'].append(time)
        attendance = json.dumps(attendance_obj)
        success = update_user_attendance(user_id, attendance, db_conn)
        return success

    except Exception as e:
        print(e)
        return False


def format_attendance_object(date_strings_list, attendance_obj):
    if date_strings_list[0] in attendance_obj:
        if date_strings_list[1] in attendance_obj[date_strings_list[0]]:
            if date_strings_list[2] in attendance_obj[date_strings_list[0]][date_strings_list[1]]:
                pass
            else:
                attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]] = {'entrance': [], 'leave': []}
        else:
            attendance_obj[date_strings_list[0]][date_strings_list[1]] = {
                date_strings_list[2]: {'entrance': [], 'leave': []}}
    else:
        attendance_obj[date_strings_list[0]] = {date_strings_list[1]: {date_strings_list[2]: {'entrance': [], 'leave': []}}}
    return attendance_obj
