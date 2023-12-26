import cv2
import numpy as np


class CircularImagesBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []
        self.index = 0

    def add(self, image):
        if len(self.buffer) < self.size:
            self.buffer.append(image)
        else:
            self.buffer[self.index] = image
        self.index = (self.index + 1) % self.size

    def get(self):
        return self.buffer

    def get_grey_image(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def get_average_difference(self, new_image):
        grey_image = self.get_grey_image(new_image)
        if len(self.buffer) == 0:
            self.add(grey_image)
            return 0
        elif len(self.buffer) < self.size:
            difference = np.mean([cv2.absdiff(image, grey_image) for image in self.buffer[:len(self.buffer)]])
            self.add(grey_image)
            return difference
        else:
            difference = np.mean([cv2.absdiff(image, grey_image) for image in self.buffer])
            self.add(grey_image)
            return difference

    def change_detected(self, new_image, threshold=15):
        return self.get_average_difference(new_image) > threshold