import face_recognition
import cv2


def get_encoding_n_image_from_cam():
    web_cam = cv2.VideoCapture(0)
    success, img = web_cam.read()
    scaled_down_img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    color_corrected_img = cv2.cvtColor(scaled_down_img, cv2.COLOR_BGR2RGB)
    image_encoding = face_recognition.face_encodings(color_corrected_img)[0]
    return img, image_encoding

def get_encoding_from_cam():
    return get_encoding_n_image_from_cam()[1]


# img, image_encoding = get_encoding_n_image_from_cam()
# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# print(image_encoding.tolist())


