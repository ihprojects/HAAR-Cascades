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



        self._layout =1


        self.add_random_stuff()
        self.detected_persons = 0

        self.detection_area = (0, 0, self.vid_player.screen_size[1], self.vid_player.screen_size[0])
        self.detection_area_color = (200,100,50)
        self.logging_table = []
        self.operation_mode = 2

        self.set_events()

        self.none_face_counter = 0
        self.face_counter = 0
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

    # @logging_table.setter
    def set_logging_table(self, looking_time):
        date_time = str(datetime.datetime.now())
        self.logging_table.append([looking_time,date_time,self._layout])


    def detec_person(self, faces, detected_faces):

        offset_x, offset_y, offset_width, offset_height = self.detection_area
        len_detected_faces = len(detected_faces)
        temp_list = []
        x_range =30
        y_range = offset_y


        for (x, y, w, h) in faces:
            diff_x = None
            diff_y = None

            if len_detected_faces != 0:
                for i,(x_old, y_old,time_stamp1) in enumerate(detected_faces):
                    x_difference = abs(x_old - x)
                    if x_difference < x_range:
                        diff_y = abs(y - y_old)
                        diff_x = abs(x - y_old)
                        temp_list+= [i]
                        break

            if diff_y == None and diff_x == None:
                diff_x = offset_width + 1
                diff_y = offset_height + 1

            if diff_x > x_range and diff_y > y_range:
                detected_faces += [(x, y,datetime.datetime.now())]
                self.detected_persons += 1

        if len(temp_list) > 0:

            reference_set = {i for i in range(0, len(detected_faces))}
            temp_set = set(temp_list)
            difference_set = reference_set.difference(temp_set)

            for i in difference_set:
                self.set_logging_table(
                    datetime.timedelta.total_seconds(datetime.datetime.now() - detected_faces[i][2]))
                detected_faces.remove(detected_faces[i])

    # passing the video player and detector objects as arguments
    def process_frame(self, dtc):

        if len(dtc.rects) == 0:
            self.none_face_counter += 1
            self.face_counter = 0
        else:
            self.face_counter += 1
            self.none_face_counter = 0

        if self.none_face_counter == self.vid_player.fps:
            self.none_face_counter = 0

            if len(self.detected_faces)>0:
                for face in self.detected_faces:
                    self.set_logging_table(datetime.timedelta.total_seconds(datetime.datetime.now()-face[2]))
            self.detected_faces = []

        for x, y, w, h in dtc.rects:
            area = self.detection_area
            if x> area[0] and y > area[1] and ((x+w) <= (area[0]+area[2])) and ((y+h) <= (area[1]+area[3])):
                # print(f"x {(x) } w {w} area[0]{area[0]} area 2 {area[2]}")
                cv2.rectangle(self.vid_player.frame, (x, y), (x + w, y + h), dtc.color.value, dtc.rect_border_size.value)

        if self.operation_mode == 1:
            self.draw_detection_area()

        elif self.operation_mode == 2:
            if self.face_counter >= self.vid_player.fps:
                self.detec_person(dtc.rects, self.detected_faces)

        # export the logging data
        if len(self.logging_table) >= 50:
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

        self.diagramm.set_labels("Title", "Duration", self.combo_date.cb.currentText())
        self.diagramm.draw_graph(x_axis, y_axis)
        # if self.diagramm.is_plotted:
        #     self.diagramm.update()
        #     self.diagrammLayout.removeWidget( self.current_diag)
        #     self.current_diag = self.diagramm.UiComponents(x_axis, y_axis, "Layouts", 0, 5)
        #     self.diagrammLayout.addWidget(self.current_diag)
        # else:
        #     self.diagramm.is_plotted = True
        #     if self.combo_layouts._selectedIndex == 4:
        #         self.current_diag = self.diagramm.UiComponents(x_axis, y_axis, "Layouts", 0, 5)
        #         self.diagrammLayout.addWidget(self.current_diag)
        #
        #     else:
        #         self.current_diag = self.diagramm.UiComponents(x_axis, y_axis, "day")
        #         self.diagrammLayout.addWidget(self.current_diag)





