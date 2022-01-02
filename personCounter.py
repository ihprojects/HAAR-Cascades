from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import datetime
import uiPersonCounter
import cv2
import fileHandler
import settings
import detector


class Scenario(QWidget):
    def __init__(self):
        super(Scenario, self).__init__()
        self.name = "No Scenario selected"

    #basic version of scenario; just draw rectangles on video frame
    def process_frame(self, vid_player, dtc):
        for rect in dtc.rects:
            cv2.rectangle(vid_player.frame, rect, dtc.color.value, dtc.rect_border_size.value)


class PersonCounter(Scenario):
    def __init__(self, detection_area=(0, 0, 100, 200)):
        super().__init__()
        self.name = "Person Counter"
        self.ui = uiPersonCounter.Ui_Form()
        self.ui.setupUi(self)
        self.ui.comboBox_mode.addItem("Count",1)
        self.ui.comboBox_mode.addItem("Calibration", 2)
        self.operation_mode = self.ui.comboBox_mode.currentData()
        self.sliders = [self.ui.sld_pos_x, self.ui.sld_pos_y, self.ui.sld_size_x, self.ui.sld_size_y]

        self.add_random_stuff()
        self.detected_persons = 0

        self.detection_area = detection_area
        self.logging_table = []
        self.operation_mode = 2

        self.set_events()

        self.none_face_counter = 0
        self.face_counter = 0
        # self._person_detector = person_counter
        self.detected_faces =[]

    def set_events(self):
        self.ui.comboBox_mode.currentIndexChanged.connect(self.change_mode)
        for slider, i in zip(self.sliders, range(len(self.sliders))):
            slider.setValue(self.detection_area[i])
            slider.valueChanged.connect(self.change_detection_area)




    # @logging_table.setter
    def logging_table(self, count):
        x = str(datetime.datetime.now().time())
        y = str(datetime.datetime.now().date())
        self._logging_table.append([str(count), x, y])


    def detec_person(self, faces, detected_faces):

        offset_x, offset_y, offset_width, offset_height = self.detection_area
        print(self.detection_area)
        number_of_person_old = self.detected_persons

        for (x, y, w, h) in faces:
            diff_x = None
            diff_y = None

            if len(detected_faces) != 0:
                for (x_old, y_old) in detected_faces:
                    x_difference = abs(x_old - x)

                    if x_difference < 30:
                        diff_y = abs(y - y_old)
                        diff_x = abs(x - y_old)
                        break

            if diff_y == None and diff_x == None:
                diff_x = offset_width + 1
                diff_y = offset_height + 1

            if diff_x > offset_width // 3 and diff_y > offset_y:
                detected_faces += [(x, y)]
                self.detected_persons += 1
                # self.logging_table = self.detected_persons - number_of_person_old

# passing the video player and detector objects as arguments
    def process_frame(self, vid_player, dtc):

        offset_x, offset_y, width_detection_area, height_detection_area = self.detection_area
        #sub_frame = vid_player.frame[offset_y:height_detection_area + offset_y, offset_x:width_detection_area + offset_x, :]
        # gray = cv2.cvtColor(sub_frame, cv2.COLOR_BGR2GRAY)
        # faces = self._person_detector.cascade_classifier.detectMultiScale(gray, 1.5, 4)

        if len(dtc.rects) == 0:
            self.none_face_counter += 1
            self.face_counter = 0
        else:
            self.face_counter += 1
            none_face_counter = 0

        if self.none_face_counter == vid_player.fps:
            none_face_counter = 0
            self.detected_faces = []

        for x, y, w, h in dtc.rects:
            x += offset_x
            y += offset_y
            cv2.rectangle(vid_player.frame, (x, y), (x + w, y + h), dtc.color.value, dtc.rect_border_size.value)

        if self.operation_mode == 1:
            cv2.rectangle(vid_player.frame, (offset_x, offset_y), (width_detection_area, height_detection_area),
                          dtc.color.value, dtc.rect_border_size.value)

        elif self.operation_mode == 2:
            if self.face_counter >= vid_player.fps:
                self.detec_person(dtc.rects, self.detected_faces)

        elif self.person_detector.operation_mode == 3:
            pass

        # export the logging data
        if len(self.logging_table) >= 50:
            is_successful = fileHandler.FileHandler.create_csv(settings.FILE_PATH_CSV, self._person_detector.logging_table)
            if is_successful:
                self.logging_table = []


    def change_mode(self):
        self.operation_mode = self.ui.comboBox_mode.currentData()
        print(self.operation_mode)

    def change_detection_area(self):
        self.detection_area = (self.sliders[0].value, self.sliders[1].value, self.sliders[2].value, self.sliders[3].value)





    ### this is how u can add ui elements and connect them to functions ###

    def add_random_stuff(self):
        #step1 create button
        btn_test1= QPushButton("test1")
        #step2 add to layout
        self.ui.lay_hor.addWidget(btn_test1)
        #step3 connect click event to function
        btn_test1.clicked.connect(self.button_clicked)

    def button_clicked(self):
        #add other element

        #we can also add widgets at specific positons
            new_label = QLabel()
            new_label.setText(f"label_at_index2")
            self.ui.lay_hor.insertWidget(2, new_label)

        #our layout now holds the following elements:
        # index 0 : a vertical layout which holds sliders etc
        # index 1: a invisible spacer; widegets on left side get pushed to the left, those on right side to the right
        # index 2: the new creaTED QLabel
        # index 3 : btn_test1