

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
    def __init__(self, signals, name, value, widget, *args): #https://www.agiliq.com/blog/2012/06/understanding-args-and-kwargs/

        self.sigs = signals
        self.name_label = QLabel(name)
        self.ui_element = widget()
        self.value = value
        # self.value_change_signal = None

        if type(self.ui_element) is QSpinBox or type(self.ui_element) is QDoubleSpinBox:
            self.ui_element.setMinimum(args[0])
            self.ui_element.setMaximum(args[1])
            self.ui_element.setSingleStep(args[2])

            self.ui_element.valueChanged.connect(self.change_value)

        if self.name_label.text() == "Color":
            self.ui_element.clicked.connect(self.change_color_value)
            self.ui_element.setStyleSheet(f"background-color: rgb({value[2]}, {value[1]}, {value[0]});")

        self.name_label.setMinimumSize(QSize(self.MIN_WIDTH_LABEL, 0))
        self.ui_element.setMinimumSize(QSize(self.MIN_WIDTH_WIDGET, 0))

    def change_value(self):
        self.value =self.ui_element.value()

    def change_color_value(self):
        self.sigs.pls_pause.emit()

        color = QColorDialog().getColor()
        q_rgb = color.rgb()
        rgb = (qBlue(q_rgb), qGreen(q_rgb), qRed(q_rgb))  # order swapped, just opencv things
        self.value = rgb
        self.ui_element.setStyleSheet(f"background-color: rgb({rgb[2]}, {rgb[1]}, {rgb[0]});")
        self.sigs.pls_resume.emit()

class Detector(QWidget):
    def __init__(self, signals, name, init_arg, tab_widget, color):

        super().__init__()
        self.sigs = signals
        self.name = name
        self.tab_widget = tab_widget
        self.rects = []
        self.classes = {"name of object to find": "argument for init_detector method"}
        self.color = DetectorParameter(self.sigs, "Color", color, QPushButton)
        self.rect_border_size = DetectorParameter(self.sigs, "Border Size", 2, QSpinBox, 1, 50, 1)
        self.is_active = True

        # parameters in this list get an ui element to tune them
        self.tunable_params =[self.color, self.rect_border_size]

        self.layout_main = QVBoxLayout(self)
        self.layout_param_outer = QHBoxLayout()
        self.layout_param_inner = QVBoxLayout()

        self.btn_destroy = QPushButton("x")
        self.btn_destroy.clicked.connect(self.destroy)

        self.q_color_dialog = QColorDialog()




    def init_ui(self):
        layout_for_destroy_button = QHBoxLayout()
        layout_for_destroy_button.addWidget(QLabel(self.name))
        layout_for_destroy_button.addStretch()
        layout_for_destroy_button.addWidget(self.btn_destroy)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)

        check_box_active = QCheckBox("Active")
        check_box_active.setChecked(True)
        check_box_active.stateChanged.connect(self.toggle_active)

        # tunable parameter ui elemnts
        self.layout_param_outer.addLayout(self.layout_param_inner)
        self.layout_param_outer.addStretch()
        for prop in self.tunable_params:
            lay_hor = QHBoxLayout()
            self.layout_param_inner.addLayout(lay_hor)

            lay_hor.addWidget(prop.name_label)
            lay_hor.addSpacing(200)
            lay_hor.addWidget(prop.ui_element)



        self.layout_main.addLayout(layout_for_destroy_button)
        self.layout_main.addWidget(line)
        self.layout_main.addWidget(check_box_active)
        self.layout_main.addSpacing(50)
        self.layout_main.addLayout(self.layout_param_outer)

        self.layout_main.addStretch()




    def destroy(self):
        self.tab_widget.removeTab(self.tab_widget.indexOf(self))
    def get_rects(self, frame):
        pass
    def init_detector(self, arg):
        pass
    def toggle_active(self):
        self.is_active = not self.is_active



