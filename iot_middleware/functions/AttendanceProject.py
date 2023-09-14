import cv2
import numpy as np
import os
from liveness_checker import test
import face_recognition


# path = "employees"
# images = []
# employees_list = os.listdir(path)
# employee_name_list = []

# for employee in employees_list:
#     curr_img = cv2.imread(f"{path}/{employee}")
#     images.append(curr_img)
#     employee_name_list.append(employee.split(".")[0])


# def find_encodings(images:list) -> list:
#     encode_list=[]
#
#     for img in images:
#         color_corrected_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#         encode_img = face_recognition.face_encodings(color_corrected_img)[0]
#         encode_list.append(encode_img)
#
#     return encode_list


# encoded_employee_images = find_encodings(images=images)
# print("Encoding Completed...")
#
# web_cam = cv2.VideoCapture(0)
#
# while True:
#     success, img = web_cam.read()
#     scaled_down_img = cv2.resize(img, (0,0),None,0.25,0.25)
#     color_corrected_img = cv2.cvtColor(scaled_down_img,cv2.COLOR_BGR2RGB)
#
#     current_directory = os.path.dirname(__file__)
#     model_dir = os.path.join(current_directory, "resources\\anti_spoof_models")
#     liveness,value =test(image=color_corrected_img, model_dir=model_dir, device_id=0)
#
#
#     if liveness == 1 :
#
#         face_locations = face_recognition.face_locations(color_corrected_img)
#         encoded_curr_img = face_recognition.face_encodings(color_corrected_img,face_locations)
#
#         for encoded_face, face_loc in zip(encoded_curr_img,face_locations):
#             compare_faces = face_recognition.compare_faces(encoded_employee_images,encoded_face)
#             face_distances = face_recognition.face_distance(encoded_employee_images,encoded_face)
#
#             match_index = np.argmin(face_distances)
#
#             if compare_faces[match_index]:
#                 name = employee_name_list[match_index].upper()
#                 print(name,f"score:{value}")
#
#
#         # cv2.imshow("webcam",img)
#
#         cv2.waitKey(1)
#     else:
#         print(f"This image is fake, score:{value}")

