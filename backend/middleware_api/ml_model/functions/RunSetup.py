from modules.DatabaseQueries import get_users_encodings_from_database, insert_attendance_record_to_database
from modules.SnapshotsQueue import SnapshotsQueue
from modules.ApiCalls import check_registration_validity
from liveness_checker import test
import face_recognition
import numpy as np
import datetime
import cv2
import os



def run_setup(entrance, num_snaps):
    if not check_registration_validity():
        print('registration_invalid !')
        return False
    snapshots_queue = SnapshotsQueue(num_snaps)
    last_snap_index = None

    users_data = get_users_encodings_from_database()
    users_encodings = [user_data['encodings'] for user_data in users_data]

    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.dirname(current_directory)
    liveness_model_dir = os.path.join(parent_directory, "resources\\anti_spoof_models")

    print("loading completed...")
    web_cam = cv2.VideoCapture(0)

    while True:
        success, img = web_cam.read()
        scaled_down_img = cv2.resize(img, (0,0),None,0.25,0.25)
        color_corrected_img = cv2.cvtColor(scaled_down_img,cv2.COLOR_BGR2RGB)
        liveness, value = test(image=color_corrected_img, model_dir=liveness_model_dir, device_id=0)

        if liveness == 1 :
            face_locations = face_recognition.face_locations(color_corrected_img)
            encoded_curr_img = face_recognition.face_encodings(color_corrected_img,face_locations)

            for encoded_face, face_loc in zip(encoded_curr_img, face_locations):
                compare_faces = face_recognition.compare_faces(users_encodings, encoded_face)
                face_distances = face_recognition.face_distance(users_encodings, encoded_face)
                match_index = np.argmin(face_distances)
                if compare_faces[match_index]:
                    snapshots_queue.shift(match_index)
                if snapshots_queue.all_items_same():
                    if last_snap_index!= match_index:
                        print("New Detection")
                        user_data = users_data[match_index]
                        current_datetime = datetime.datetime.now()
                        current_time = current_datetime.strftime("%H-%M")
                        current_date = current_datetime.strftime("%Y-%m-%d")
                        insert_attendance_record_to_database(user_data['backend_id'], user_data['user_api_code'], current_date, current_time, entrance)
                    last_snap_index = match_index

            # cv2.imshow("webcam",img)
            cv2.waitKey(1)
        else:
            print(f"This image is fake, score:{value}")



# run_setup(True, 3)