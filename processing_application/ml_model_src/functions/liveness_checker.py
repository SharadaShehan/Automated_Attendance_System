import os
import numpy as np
import warnings
import time

from middleware_api.ml_model_src.src.anti_spoof_predict import AntiSpoofPredict
from middleware_api.ml_model_src.src.generate_patches import CropImage
from middleware_api.ml_model_src.src.utility import parse_model_name

warnings.filterwarnings('ignore')

# SAMPLE_IMAGE_PATH = "./images/sample/"


def test(image, model_dir, device_id:int)->(int,float):
    model_test = AntiSpoofPredict(device_id)
    image_cropper = CropImage()

    image_bbox = model_test.get_bbox(image)
    prediction = np.zeros((1, 3))
    test_speed = 0
    # sum the prediction from single model's result
    for model_name in os.listdir(model_dir):
        h_input, w_input, model_type, scale = parse_model_name(model_name)
        param = {
            "org_img": image,
            "bbox": image_bbox,
            "scale": scale,
            "out_w": w_input,
            "out_h": h_input,
            "crop": True,
        }
        if scale is None:
            param["crop"] = False
        img = image_cropper.crop(**param)
        start = time.time()
        prediction += model_test.predict(img, os.path.join(model_dir, model_name))
        test_speed += time.time()-start

    # draw result of prediction
    label = np.argmax(prediction)
    value = prediction[0][label]/2
    return label,value



