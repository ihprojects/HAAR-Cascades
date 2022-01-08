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
import pyqtgraph as pg

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

        self.cal = CalendarUI.MyDatePicker()
        self.combo_date = ComboBoxUi.MyCombobox()
        self.combo_layouts = ComboBoxUi.MyCombobox()

        self.diagrammLayout = QVBoxLayout()
        self.diagramm = graphPlotter.GraphPlotter(self.diagrammLayout)
        # self.diagrammLayout.addWidget(self.diagramm)


        self.add_random_stuff()
        self.detected_persons = 0

        self.detection_area = (0, 0, self.vid_player.frame_size[1], self.vid_player.frame_size[0])
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
            self.sliders[i].setMaximum(self.vid_player.frame_size[i])
            self.sliders[i].setValue(self.vid_player.frame_size[i] // 2)

        for i in range(2,4):
            self.sliders[i].setMinimum(0)
            self.sliders[i].setMaximum(self.vid_player.frame_size[i - 2])
            self.sliders[i].setValue(self.vid_player.frame_size[i - 2])
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
    # addWidget (self, QWidget, row, column, rowSpan, columnSpan, Qt.Alignment alignment = 0)
    def add_random_stuff(self):

        # Layouts
        command_layout = QVBoxLayout()
        # plot_layout = QVBoxLayout()
        self.ui.lay_hor.addLayout(command_layout)
        self.ui.lay_hor.addLayout(self.diagrammLayout)





        # Widgets

        submit_btn = QPushButton("Submitt")
        submit_btn.clicked.connect(self.button_clicked)

        label = QLabel("Statistik")

        # plot_layout.addWidget(label)
        self.diagrammLayout.addWidget(label)
        # plot_layout.addWidget(self.diagramm._widget)
        command_layout.addWidget(self.combo_date.initUI(["day", "month", "year"], "Selected periode"))
        command_layout.addWidget(self.cal.initUI("selected Date"))
        command_layout.addWidget(
            self.combo_layouts.initUI(["Layout 1", "Layout 2", "Layout 3", "Layout 4", "All"], "selected Layout"))
        command_layout.addWidget(submit_btn)

    # https://stackoverflow.com/questions/61449954/pyqt5-datepicker-popup

    def button_clicked(self):
        stati = Statistic.Statistic()
        x_axis, y_axis = stati.getDataOfSpecificDate(self.cal._selectedDate, self.combo_date._selectedIndex,self.combo_layouts._selectedIndex)

        self.diagramm.set_labels("Title", self.combo_date.cb.currentText(), "Duration")
        self.diagramm.draw_graph(x_axis, y_axis)
        # self.diagrammLayout.addWidget(pg.plot())
        # self.diagrammLayout.addWidget(Diagramm.Diagram(self.diagrammLayout))
        # if self.diagramm.is_plotted:
        #     # self.diagramm.update()
        #
        #     self.diagramm.draw_graph(x_axis, y_axis, "Layouts", 0, 5)
        #     self.diagrammLayout.removeWidget( self.current_diag)
        #     self.current_diag = self.diagramm.UiComponents(x_axis, y_axis, "Layouts", 0, 5)
        #     self.diagrammLayout.addWidget(self.current_diag)
        #     print("yo")
        # else:
        #     self.diagramm.is_plotted = True
        #     if self.combo_layouts._selectedIndex == 4:
        #         self.current_diag = self.diagramm.UiComponents(x_axis, y_axis, "Layouts", 0, 5)
        #         self.diagrammLayout.addWidget(self.current_diag)
        #
        #     else:
        #         self.current_diag = self.diagramm.UiComponents(x_axis, y_axis, "day")
        #         self.diagrammLayout.addWidget(self.current_diag)





