from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import detectorHOG, detectorHAAR

# QLineEdit { border: 1px solid white }
class DetectorManager(QWidget):
#    available_detectors = {"HAAR Cascade": detectorHAAR.HAARCascades, "HOG": detectorHOG.HOGDetector}
    def __init__(self, main_win):
        super().__init__()
        self.detectors =[]
        # self.addTab(detector.Detector("",""),"abc")
        # self.add_detector()
        self.main_win = main_win
        self.layout_main = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.layout_add = QHBoxLayout()
        self.btn_add = QPushButton("Add")
        self.c_box_select_detector = QComboBox()
        self.c_box_class2find = QComboBox()


        self.layout_main.addWidget(self.tab_widget)
        self.layout_main.addLayout(self.layout_add)

        self.layout_add.addWidget(self.c_box_select_detector)
        self.layout_add.addWidget(self.c_box_class2find)
        self.layout_add.addStretch()
        self.layout_add.addWidget(self.btn_add)

        '''''


        for dtc in self.available_detectors.keys():
            self.c_box_select_detector.addItem(dtc, self.available_detectors[dtc])
        self.fill_class_selection_box()
        self.c_box_select_detector.currentIndexChanged.connect(self.select_detector)'''

        self.btn_add.setStyleSheet("background-color: rgb(10, 94, 22)")#; color: rgb(0, 0, 0);")

        self.btn_add.clicked.connect(self.add_detector)
    def fill_class_selection_box(self):
        for cls in self.c_box_select_detector.currentData().detectable_objects.keys():
            self.c_box_class2find.addItem(cls, self.c_box_select_detector.currentData().detectable_objects[cls])

    def select_detector(self):
        self.c_box_class2find.clear()
        self.fill_class_selection_box()

    def add_detector(self):
        ref = self.c_box_select_detector.currentData()
        dtc = ref(self.main_win,self.c_box_class2find.currentText(),self.c_box_class2find.currentData(), self.tab_widget)
        self.tab_widget.addTab(dtc, self.c_box_select_detector.currentText())
    def get_detectors(self):
        # https://stackoverflow.com/questions/6167196/get-all-tabs-widgets-in-qtabwidget
        detectors = []
        for i in range(0,self.tab_widget.count()):
            detectors.append(self.tab_widget.widget(i))
        return detectors
