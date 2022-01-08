import detector
import cv2
import numpy as np
import dlib

class HOGDetector(detector.Detector):
    detectable_objects = {"Face" : dlib.get_frontal_face_detector}

    def __init__(self, signals, name, init_arg, tab_widget, color):
        super().__init__(signals, name, init_arg, tab_widget, color)
        self.detector = init_arg()
        self.init_ui()

    def get_rects(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        im = np.float32(gray_frame) / 255.0
        self.rects =[]
        #https://python.hotexamples.com/examples/dlib/-/get_frontal_face_detector
        # /python-get_frontal_face_detector-function-examples.html
        rect_corners = self.detector(frame, 0)
        for rect in rect_corners:
            self.rects.append((rect.left(), rect.top(),rect.right()- rect.left(),rect.bottom()- rect.top()))
