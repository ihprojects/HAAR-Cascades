from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from random import randint

import detectorHOG, detectorHAAR


class DetectorManager(QWidget):

    AVAILABLE_DETECTORS = {"HAAR Cascade": detectorHAAR.HAARCascades, "HOG": detectorHOG.HOGDetector}
    FAVORITE_COLORS = [(230, 50, 20), (40, 220, 31), (10, 20, 244), (10, 170, 204)]

    def __init__(self, signals):
        super().__init__()
        self.sigs = signals

        self.layout_main = QVBoxLayout(self)
        self.tab_widget = QTabWidget()         # detectors are added as tabs to this widget

        self.init_ui()


    def init_ui(self):

        layout_add = QHBoxLayout()
        self.c_box_select_detector = QComboBox()
        self.c_box_class2find = QComboBox()

        btn_add = QPushButton("Add")
        btn_add.setStyleSheet("background-color: rgb(10, 94, 22)")

        layout_add.addWidget(self.c_box_select_detector)
        layout_add.addWidget(self.c_box_class2find)
        layout_add.addStretch()
        layout_add.addWidget(btn_add)

        for dtc in self.AVAILABLE_DETECTORS.keys():
            self.c_box_select_detector.addItem(dtc, self.AVAILABLE_DETECTORS[dtc])
        self.fill_class_selection_box()


        #connect
        self.c_box_select_detector.currentIndexChanged.connect(self.fill_class_selection_box)
        btn_add.clicked.connect(self.add_detector)

        #add to main layout
        self.layout_main.addWidget(self.tab_widget)
        self.layout_main.addLayout(layout_add)

    def fill_class_selection_box(self):
        self.c_box_class2find.clear()
        for cls in self.c_box_select_detector.currentData().detectable_objects.keys():
            self.c_box_class2find.addItem(cls, self.c_box_select_detector.currentData().detectable_objects[cls])

    def add_detector(self):
        if self.tab_widget.count() < len(self.FAVORITE_COLORS):
            color = self.FAVORITE_COLORS[self.tab_widget.count()]
        else:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        ref = self.c_box_select_detector.currentData()
        #Detector init signature: def __init__(self, signals, name, init_arg, tab_widget, color)
        dtc = ref(self.sigs, self.c_box_class2find.currentText(),self.c_box_class2find.currentData(),
                  self.tab_widget, color)
        self.tab_widget.addTab(dtc, self.c_box_select_detector.currentText())
        self.tab_widget.setCurrentWidget(dtc)

    def get_detectors(self):
        # https://stackoverflow.com/questions/6167196/get-all-tabs-widgets-in-qtabwidget
        detectors = []
        for i in range(0,self.tab_widget.count()):
            detectors.append(self.tab_widget.widget(i))
        return detectors
