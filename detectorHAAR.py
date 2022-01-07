import detector
import cv2
from PyQt5.QtWidgets import *

class HAARCascades(detector.Detector):
    detectable_objects = {"Frontal face v1": "haarcascade_frontalface_alt.xml",
                        "Frontal face v2": "haarcascade_frontalface_alt2.xml",
                        "Frontal face default": "haarcascade_frontalface_default.xml",
                        "Fullbody": "haarcascade_fullbody.xml"}

    def __init__(self, main_win, name, init_arg, tab_widget):
        super().__init__(main_win, name, init_arg, tab_widget)
        path = "data/"
        print(init_arg)
        self.classifier = cv2.CascadeClassifier(path+init_arg)
        self.scale_factor = detector.DetectorParameter(self.main_win,"Scale Factor", 1.2, QDoubleSpinBox, 1.1, 2.0, 0.1)
        self.min_neighbors = detector.DetectorParameter(self.main_win, "min Neighbors", 5, QSpinBox, 1, 20, 1)
        self.min_size_x = detector.DetectorParameter(self.main_win, "min Size X", 50, QSpinBox, 1, 200, 1)
        self.min_size_y = detector.DetectorParameter(self.main_win, "min Size Y", 50, QSpinBox, 1, 200, 1)
        self.flags = cv2.CASCADE_SCALE_IMAGE

        #parameters in this list get an ui element to tune them
        self.tunable_params = self.tunable_params + [self.scale_factor, self.min_neighbors]
        self.add_props()
    def get_rects(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.rects = self.classifier.detectMultiScale(gray_frame, scaleFactor=self.scale_factor.value,
                                                      minNeighbors=self.min_neighbors.value,
                                                      minSize=(self.min_size_x.value, self.min_size_y.value),
                                                      flags=self.flags)


    def init_detector(self, arg):
        self.classifier = cv2.CascadeClassifier(arg)

