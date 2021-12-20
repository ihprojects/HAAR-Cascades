import cv2
from datetime import datetime
from PyQt5.QtWidgets import *
import statusController
class Detector():
    # def __init__(self,  name, conf_file, color, s_controller, id):
    def __init__(self, name, conf_file, color, s_controller, lbl):
        self.name = name
        self.orig_frame = None
        # self.rects = []
        self.color = color
        self.rect_border_size = 2
        self.classifier = None
        self.is_active = True
        self.conf_file = conf_file
        # self.id = id
        self.s_controller = s_controller
        self.label = lbl

    def get_rects(self, frame):
        pass

    def set_label(self, delta_t):
        pass

# 'haarcascade_fullbody.xml'
class HAARcascades(Detector):
    # def __init__(self, name, conf_file, color, s_controller, id):
    def __init__(self, name, conf_file, color, s_controller, lbl):
        # super.__init__()
        # super().__init__( name, conf_file, color, s_controller , id)
        super().__init__( name, conf_file, color, s_controller , lbl)
        # self.classifier_xml_names = {'HAAR_full_body': 'haarcascade_fullbody.xml', 'HAAR_face': 'haarcascade_frontalface_alt.xml'}
        self.classifier = cv2.CascadeClassifier(self.conf_file)
        self.scale_factor = 1.2
        self.min_neighbors = 5
        self.min_size = (50,50)
        self.flags = cv2.CASCADE_SCALE_IMAGE
        self.set_label(0)
    def get_rects(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        t_0 = datetime.now()
        rects = self.classifier.detectMultiScale(gray_frame, scaleFactor=self.scale_factor,
                                                 minNeighbors=self.min_neighbors, minSize=self.min_size,
                                                 flags=self.flags)

        time_to_get_rects= int((t_0- datetime.now()).total_seconds() *1000)
        self.set_label(time_to_get_rects)
        return rects

    def set_label(self, delta_t):
        # self.s_controller.labels[self.id].setText(f'{self.name}: {str(delta_t)} ms')
        self.label.setText(f'{self.name}: {str(delta_t)} ms')