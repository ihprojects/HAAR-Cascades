from random import randint

import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial

import mainWindow
import settings


class DetectorParameter:
    MIN_WIDTH_LABEL = 120
    MIN_WIDTH_WIDGET = 80
    def __init__(self, main_win, name, value, widget, *args): #https://www.agiliq.com/blog/2012/06/understanding-args-and-kwargs/
        self.main_win = main_win
        self.label =QLabel(name)
        self.widget = widget()
        self.value = value
        self.value_change_signal = None

        if type(self.widget) is QSpinBox or type(self.widget) is QDoubleSpinBox:
            self.widget.setMinimum(args[0])
            self.widget.setMaximum(args[1])
            self.widget.valueChanged.connect(self.change_value)

        if self.label.text() == "Color":
            self.widget.clicked.connect(self.change_color_value)

        self.label.setMinimumSize(QSize(self.MIN_WIDTH_LABEL, 0))
        self.widget.setMinimumSize(QSize(self.MIN_WIDTH_WIDGET, 0))

    def change_value(self):
        self.value =self.widget.value()
    def change_color_value(self):
        self.main_win.pls_pause.emit()
        color = QColorDialog().getColor()

        # self.q_color_dialog.selectedColor = color
        q_rgb = color.rgb()
        rgb = (qBlue(q_rgb), qGreen(q_rgb), qRed(q_rgb))  # order swapped, just opencv things
        self.value = rgb
        self.widget.setStyleSheet(f"background-color: rgb({rgb[2]}, {rgb[1]}, {rgb[0]});")
        self.main_win.pls_resume.emit()
class Detector(QWidget):
    def __init__(self, main_win, name, init_arg, tab_widget):

        super().__init__()

        self.main_win = main_win
        self.name = name
        self.tab_widget = tab_widget
        self.rects = []
        self.classes = {"name of object to find": "argument for init_detector method"}
        self.color = DetectorParameter(self.main_win, "Color", (randint(0, 255),randint(0, 255), randint(0, 255)), QPushButton)
        self.rect_border_size = DetectorParameter(self.main_win, "Border Size", 2, QSpinBox, 1, 50, 1)
        self.classifier = None
        self.is_active = True
        self.tunable_params =[self.color, self.rect_border_size]


        self.layout_main = QVBoxLayout(self)


        self.layout_param_outer = QHBoxLayout()
        self.layout_param_inner = QVBoxLayout()


        # self.btn_add = QPushButton("Add")
        self.btn_destroy = QPushButton("x")
        self.btn_destroy.clicked.connect(self.destroy)

        self.init_ui()



        self.q_color_dialog = QColorDialog()
        self.q_color_dialog.setWindowFlags(Qt.WindowStaysOnTopHint)



    def init_ui(self):
        lay_hor = QHBoxLayout()
        lay_hor.addWidget(QLabel(self.name))
        # lay_hor.addSpacing(200)
        lay_hor.addStretch()
        lay_hor.addWidget(self.btn_destroy)

        self.layout_main.addLayout(lay_hor)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        self.layout_main.addWidget(line)
        check_box_active = QCheckBox("Active")
        check_box_active.setChecked(True)
        check_box_active.stateChanged.connect(self.toggle_active)
        self.layout_main.addWidget(check_box_active)

        self.layout_main.addSpacing(50)
        self.layout_main.addLayout(self.layout_param_outer)
        self.layout_param_outer.addLayout(self.layout_param_inner)
        self.layout_param_outer.addStretch()
        self.layout_main.addStretch()


    def add_props(self):
        for prop in self.tunable_params:
            lay_hor = QHBoxLayout()
            self.layout_param_inner.addLayout(lay_hor)

            lay_hor.addWidget(prop.label)
            lay_hor.addSpacing(200)
            lay_hor.addWidget(prop.widget)

    def change_value(self, widget, prop, widget_type):
        if widget_type == "spin":
            prop.value = widget.value()
        # https://stackoverflow.com/questions/53690302/qcolordialoggetcolor-function-get-rgb-value-and-conver-to-hex
        if widget_type == "color":
            self.main_win.pls_pause.emit()
            color = self.q_color_dialog.getColor()

            self.q_color_dialog.selectedColor = color
            q_rgb = color.rgb()
            rgb = (qBlue(q_rgb), qGreen(q_rgb), qRed(q_rgb))  # order swapped, just opencv things
            prop.value = rgb
            widget.setStyleSheet(f"background-color: rgb({rgb[2]}, {rgb[1]}, {rgb[0]});")
            self.main_win.pls_resume.emit()

    def destroy(self):
        self.tab_widget.removeTab(self.tab_widget.indexOf(self))
    def get_rects(self, frame):
        pass
    def init_detector(self, arg):
        pass
    def toggle_active(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True


