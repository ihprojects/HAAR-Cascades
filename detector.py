import cv2
from datetime import datetime
from PyQt5.QtWidgets import *


class DetectorParameter:
    def __init__(self, name, value, min_val, max_val, single_step, param_type):
        self.name = name
        self.value = value
        self.min_value = min_val
        self.max_value = max_val
        self.single_step = single_step
        self.type = param_type


class Detector:
    def __init__(self, color, lbl, name, conf_file):
        self.name = name
        self.rects = []
        self.color = DetectorParameter("Color", color, 0, 255, 1, "color")
        self.rect_border_size = DetectorParameter("Border Size", 2, 1, 50, 1, int)
        self.classifier = None
        self.is_active = False
        self.conf_file = conf_file
        self.label = lbl
        self.tunable_params =[self.color, self.rect_border_size]

    def get_rects(self, frame):
        pass

    def toggle_active(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True


class HAARCascades(Detector):
    def __init__(self, color, lbl, name, conf_file):
        super().__init__(  color, lbl, name, conf_file)

        self.classifier = cv2.CascadeClassifier(self.conf_file)
        self.scale_factor = DetectorParameter("Scale Factor", 1.2, 1.1, 5.0, 0.1, float)
        self.min_neighbors = DetectorParameter("min Neighbors", 5, 1, 20, 1, int)
        self.min_size_x = DetectorParameter("min Size X", 50, 1, 200, 1, int)
        self.min_size_y = DetectorParameter("min Size Y", 50, 1, 200, 1, int)
        self.flags = cv2.CASCADE_SCALE_IMAGE

        #parameters in this list get an gui element to tune them
        self.tunable_params = self.tunable_params + [self.scale_factor, self.min_neighbors]

    def get_rects(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.rects = self.classifier.detectMultiScale(gray_frame, scaleFactor=self.scale_factor.value,
                                                      minNeighbors=self.min_neighbors.value,
                                                      minSize=(self.min_size_x.value, self.min_size_y.value),
                                                      flags=self.flags)





