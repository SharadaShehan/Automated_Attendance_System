import queue
from database.models import CustomUser
from middleware_api.ml_model_src.functions import liveness_checker
import face_recognition
import numpy as np
import datetime, cv2, os, json

class MLModel:
    pending_tasks = queue.Queue(maxsize=20)
    finished_tasks = queue.Queue()

    @classmethod
    def start_ml_model(cls):
        current_directory = os.path.dirname(__file__)
        liveness_model_dir = os.path.join(current_directory, "ml_model_src\\resources\\anti_spoof_models")
        users_data = CustomUser.objects.all().values('id', 'encodings')
        users_encodings = [user_data['encodings'] for user_data in users_data]

        while True:
            if not cls.pending_tasks.empty():
                # Get the next pending process
                task_data = cls.pending_tasks.get()
                list_image = task_data['photo']
                converted_image = np.array(list_image).astype(np.uint8)
                liveness, value = liveness_checker.test(image=converted_image, model_dir=liveness_model_dir, device_id=0)

                if liveness:
                    encoded_image = face_recognition.face_encodings(converted_image)[0]
                    distance_list = []
                    for user_encodings in users_encodings:
                        user_encodings = np.array(json.loads(user_encodings))
                        distance = face_recognition.face_distance([user_encodings], encoded_image)
                        distance_list.append(distance)
                    min_distance = min(distance_list)
                    if min_distance < 0.5:
                        user_id = users_data[distance_list.index(min_distance)]['id']
                        user = CustomUser.objects.get(id=user_id)
                        cls.finished_tasks.put({'user_name': user.first_name+" "+user.last_name, 'gender': user.gender,
                                                'liveness': liveness, 'value': value})
                    else:
                        cls.finished_tasks.put({'user_id': None, 'liveness': liveness, 'value': value})
                else:
                    cls.finished_tasks.put({'user_id': None, 'liveness': liveness, 'value': value})

    @classmethod
    def add_task(cls, input_data):
        if not cls.pending_tasks.full():
            cls.pending_tasks.put(input_data)
            return True
        return False

    @classmethod
    def get_result(cls):
        if not cls.finished_tasks.empty():
            return cls.finished_tasks.get()
        return None

