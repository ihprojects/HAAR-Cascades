from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import datetime
import uiPersonCounter
import cv2
import fileHandler
import settings
import detector
import Statistic
import graphPlotter
import CalendarUI
import ComboBoxUi


class Scenario(QWidget):
    def __init__(self, video_player):
        super(Scenario, self).__init__()
        self.name = "No Scenario selected"
        self.vid_player = video_player

    # basic version of scenario; just draw rectangles on video frame
    def process_frame(self, dtc):
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
        self.ui.comboBox_mode.addItem("Count", 2)
        self.ui.comboBox_mode.addItem("Calibration", 1)
        self.operation_mode = self.ui.comboBox_mode.currentData()
        self.sliders = [self.ui.sld_pos_x, self.ui.sld_pos_y, self.ui.sld_size_x, self.ui.sld_size_y]
        self.cal = CalendarUI.MyDatePicker()
        self.combo_date = ComboBoxUi.MyCombobox()
        self.combo_layouts = ComboBoxUi.MyCombobox()
        # self.diagramm = graphPlotter.GraphPlotter()
        self.diagrammLayout = QVBoxLayout()
        self.diagramm = graphPlotter.GraphPlotter(self.diagrammLayout)
        self._layout = 1
        self.add_random_stuff()
        self.cbox = QComboBox()
        self.cbox.addItem("Layout 1", 1)
        self.cbox.addItem("Layout 2", 2)
        self.cbox.addItem("Layout 3", 3)
        self.cbox.addItem("Layout 4", 4)
        self.ui.verticalLayout.addWidget(self.cbox)
        self.cbox.currentIndexChanged.connect(self.change_layout)
        self.detected_persons = 0
        self.detection_area = (0, 0, self.vid_player.screen_size[1], self.vid_player.screen_size[0])
        self.detection_area_color = (200, 100, 50)
        self.logging_table = []
        self.operation_mode = 2
        self.set_events()
        self.none_face_counter = 0
        self.face_counter = 0
        # self._person_detector = person_counter
        self.detected_faces = []
        self.init_ui()

    def set_events(self):
        self.ui.comboBox_mode.currentIndexChanged.connect(self.change_mode)
        for slider, i in zip(self.sliders, range(len(self.sliders))):
            slider.valueChanged.connect(self.change_detection_area)

# TODO connect with video mode change event
    def init_ui(self):

        for i in range(2):
            self.sliders[i].setMinimum(0)
            self.sliders[i].setMaximum(self.vid_player.screen_size[i])
            self.sliders[i].setValue(self.vid_player.screen_size[i] // 2)

        for i in range(2, 4):
            self.sliders[i].setMinimum(0)
            self.sliders[i].setMaximum(self.vid_player.screen_size[i - 2])
            self.sliders[i].setValue(self.vid_player.screen_size[i - 2])
        self.sliders[1].setInvertedAppearance(True)

    def change_layout(self):
        self._layout = self.cbox.currentData()
        print(self._layout)

    def set_logging_table(self, looking_time):
        date_time = datetime.datetime.now().strftime('"%Y-%m-%d %H:%M:%S"')

        # add data with duration time bigger than 1s
        if looking_time > 1:
            self.logging_table.append([looking_time, date_time, self._layout])

    def detect_duration_time(self, faces, detected_faces):

        # init
        offset_x, offset_y, offset_width, offset_height = self.detection_area
        # save the length of the detected faces
        len_detected_faces = len(detected_faces)
        temp_list = []
        x_range = 30
        y_range = offset_y

        # parse the faces
        for (x, y, w, h) in faces:
            diff_x = None
            diff_y = None

            # check, if
            if len_detected_faces != 0:

                # get the detected faces and check, if the current faces equal with the detected face
                for i, (x_old, y_old, time_stamp1) in enumerate(detected_faces):

                    # calculate the difference between x pos current face and detected face
                    x_difference = abs(x_old - x)

                    # if the difference bigger than range, then is the current face not equal with the detected face. Thats mean, it is maybe a new person
                    if x_difference < x_range:
                        diff_y = abs(y - y_old)
                        diff_x = abs(x - y_old)
                        # save the founded faces
                        temp_list += [i]
                        break

            # activate only by new faces, who not contains in the list detected face
            if diff_y == None and diff_x == None:
                diff_x = offset_width + 1
                diff_y = offset_height + 1

            # add the new face in the list of detected faces
            if diff_x > x_range and diff_y > y_range:
                detected_faces += [(x, y, datetime.datetime.now())]
                self.detected_persons += 1

        # check if the founded faces bigger than zero
        if len(temp_list) > 0:
            # create a reference set with integer items (0 - lenght of detected faces-1)
            reference_set = {i for i in range(0, len_detected_faces)}
            # create a set from the founded faces, who contains in the list of detected faces
            temp_set = set(temp_list)
            # detect the items from temp set , who not contains in reference set
            difference_set = reference_set.difference(temp_set)
            temp_value = 0

            # the items of the difference set are equal to the person who no longer looks into the camera
            # add the item to the logging table and remove from the list of the detected faces
            for i in difference_set:
                self.set_logging_table(
                    datetime.timedelta.total_seconds(datetime.datetime.now() - detected_faces[i - temp_value][2]))
                detected_faces.remove(detected_faces[i - temp_value])
                temp_value += 1

    # passing the video player and detector objects as arguments
    def process_frame(self, dtc):


        #dtc.rect = detected faces
        # count how often a face is recognized or not recognized
        if len(dtc.rects) == 0:
            self.none_face_counter += 1
            self.face_counter = 0
        else:
            self.face_counter += 1
            self.none_face_counter = 0

        if self.none_face_counter == self.vid_player.fps:
            self.none_face_counter = 0

            #Add the detected faces into the logging table
            if len(self.detected_faces) > 0:
                for face in self.detected_faces:
                    self.set_logging_table(datetime.timedelta.total_seconds(datetime.datetime.now() - face[2]))
            self.detected_faces = []


        #Adjust the rcalibration rectangle
        for x, y, w, h in dtc.rects:
            area = self.detection_area
            if x > area[0] and y > area[1] and ((x + w) <= (area[0] + area[2])) and ((y + h) <= (area[1] + area[3])):
                # print(f"x {(x) } w {w} area[0]{area[0]} area 2 {area[2]}")
                cv2.rectangle(self.vid_player.frame, (x, y), (x + w, y + h), dtc.color.value,
                              dtc.rect_border_size.value)

        #opmode =1 calibration mode : Show only the calibration angle
        if self.operation_mode == 1:
            self.draw_detection_area()


        #opmode = 2 face detection mode
        elif self.operation_mode == 2:
            if self.face_counter >= self.vid_player.fps:
                self.detect_duration_time(dtc.rects, self.detected_faces)

        # export the logging data
        if len(self.logging_table) >= 3:
            is_successful = fileHandler.FileHandler.create_csv(settings.FILE_PATH_CSV, self.logging_table)
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
        self.detection_area = (max(0, x_center - width // 2),
                               max(0, y_center - height // 2),
                               width,
                               height)

    ### this is how u can add ui elements and connect them to functions ###
    # addWidget (self, QWidget, row, column, rowSpan, columnSpan, Qt.Alignment alignment = 0)
    def add_random_stuff(self):

        # Layouts
        command_layout = QVBoxLayout()
        # plot_layout = QVBoxLayout()
        self.ui.lay_hor.addLayout(command_layout)
        self.ui.lay_hor.addLayout(self.diagrammLayout)

        # Widgets
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.button_clicked)
        label = QLabel("Statistik")
        self.diagrammLayout.addWidget(label)
        # plot_layout.addWidget(self.diagramm._widget)
        command_layout.addWidget(self.combo_date.initUI(["day", "month", "year"], "Selected periode"))
        command_layout.addWidget(self.cal.initUI("selected Date"))
        command_layout.addWidget(
            self.combo_layouts.initUI(["Layout 1", "Layout 2", "Layout 3", "Layout 4", "All"], "selected Layout"))
        command_layout.addWidget(submit_btn)

    def button_clicked(self):

        #create the statistic class
        stati = Statistic.Statistic()
        x_axis, y_axis = stati.getDataOfSpecificDate(self.cal._selectedDate, self.combo_date._selectedIndex,
                                                     self.combo_layouts._selectedIndex)
        x_axis_label = "day"

        if self.combo_date.cb.currentText() == "day":
            x_axis_label = "hour"
        elif self.combo_date.cb.currentText() == "month":
            x_axis_label = "day"
        elif self.combo_date.cb.currentText() == "year":
            x_axis_label = "month"

        self.diagramm.set_labels("Title", "Duration", x_axis_label)
        self.diagramm.draw_graph(x_axis, y_axis)
