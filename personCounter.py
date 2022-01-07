from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import datetime
import uiPersonCounter
import cv2
import fileHandler
import settings
import detector


class Scenario(QWidget):
    def __init__(self, video_player):
        super(Scenario, self).__init__()
        self.name = "No Scenario selected"
        self.vid_player = video_player

    #basic version of scenario; just draw rectangles on video frame
    def process_frame(self,  dtc):
        for rect in dtc.rects:
            cv2.rectangle(self.vid_player.frame, rect, dtc.color.value, dtc.rect_border_size.value)
    def init_ui(self):
        pass

class PersonCounter(Scenario):
    def __init__(self, video_player, detection_area=(0, 0, 100, 200)):
        super().__init__(video_player)
        self.name = "Person Counter"
        self.ui = uiPersonCounter.Ui_Form()
        self.ui.setupUi(self)
        self.ui.comboBox_mode.addItem("Count",2)
        self.ui.comboBox_mode.addItem("Calibration", 1)
        self.operation_mode = self.ui.comboBox_mode.currentData()
        self.sliders = [self.ui.sld_pos_x, self.ui.sld_pos_y, self.ui.sld_size_x, self.ui.sld_size_y]

        self.add_random_stuff()
        self.detected_persons = 0

        self.detection_area = (0, 0, self.vid_player.screen_size[1], self.vid_player.screen_size[0])
        self.detection_area_color = (200,100,50)
        self.logging_table = []
        self.operation_mode = 2

        self.set_events()

        self.none_face_counter = 0
        self.face_counter = 0
        # self._person_detector = person_counter
        self.detected_faces =[]
        self.init_ui()
    def set_events(self):
        self.ui.comboBox_mode.currentIndexChanged.connect(self.change_mode)





        for slider, i in zip(self.sliders, range(len(self.sliders))):
            # slider.setValue(self.detection_area[i])
            slider.valueChanged.connect(self.change_detection_area)
#TODO connect with video mode change event
    def init_ui(self):
        for i in range(2):
            self.sliders[i].setMinimum(0)
            self.sliders[i].setMaximum(self.vid_player.screen_size[i])
            self.sliders[i].setValue(self.vid_player.screen_size[i]//2)

        for i in range(2,4):
            self.sliders[i].setMinimum(0)
            self.sliders[i].setMaximum(self.vid_player.screen_size[i-2])
            self.sliders[i].setValue(self.vid_player.screen_size[i-2])
        self.sliders[1].setInvertedAppearance(True)

    def set_detection_area(self):
        pass

    # @logging_table.setter
    def logging_table(self, count):
        x = str(datetime.datetime.now().time())
        y = str(datetime.datetime.now().date())
        self._logging_table.append([str(count), x, y])


    def detec_person(self, faces, detected_faces):

        offset_x, offset_y, offset_width, offset_height = self.detection_area

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
    def process_frame(self, dtc):

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

        if self.none_face_counter == self.vid_player.fps:
            none_face_counter = 0
            self.detected_faces = []

        for x, y, w, h in dtc.rects:
            # x += offset_x
            # y += offset_y
            area = self.detection_area
            if x> area[0] and y > area[1] and ((x+w) <= (area[0]+area[2])) and ((y+h) <= (area[1]+area[3])):
                # print(f"x {(x) } w {w} area[0]{area[0]} area 2 {area[2]}")
                cv2.rectangle(self.vid_player.frame, (x, y), (x + w, y + h), dtc.color.value, dtc.rect_border_size.value)

        if self.operation_mode == 1:
            self.draw_detection_area()
        # x_center + width // 2,
        # y_center + height // 2)

        elif self.operation_mode == 2:
            if self.face_counter >= self.vid_player.fps:
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

    def draw_detection_area(self):
        cv2.rectangle(self.vid_player.frame, self.detection_area,
                      self.detection_area_color, 4)


    def change_detection_area(self):
        x_center = self.sliders[0].value()
        y_center = self.sliders[1].value()
        width = self.sliders[2].value()
        height = self.sliders[3].value()
        self.detection_area = (max(0, x_center - width//2),
                               max(0, y_center - height//2),
                               width,
                               height)



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