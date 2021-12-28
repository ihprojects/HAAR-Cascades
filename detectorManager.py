from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import detector
import uiOptionsTab
import statusController

class options_tab(QWidget):
    def __init__(self, detector_manager, detector):
        super().__init__()
        self.ui = uiOptionsTab.Ui_Form()
        self.ui.setupUi(self)
        self.btn_add = self.ui.btn_add
        self.detector_manager = detector_manager
        self.detector = detector
        self.ui.comboBox.addItem("Setting1")
        self.ui.comboBox.addItem("Setting2")
        self.init_ui()
        self.set_events()

    def init_ui(self):
        for key in self.detector.tunable_params:
            # self.ui.verticalLayout.addWidget(QPushButton(key))
            hor_layout = QHBoxLayout()
            spin_box = QSpinBox()
            self.ui.verticalLayout.addLayout(hor_layout)
            hor_layout.addWidget(QLabel(key))
            hor_layout.addWidget(spin_box)

    # https: // stackoverflow.com / questions / 940555 / pyqt - sending - parameter - to - slot - when - connecting - to - a - signal
#https://www.tutorialspoint.com/pyqt/pyqt_qspinbox_widget.htm
    def value_change(self, property, spin_box):
        property  = spin_box.value()

    def set_events(self):
        self.btn_add.clicked.connect(self.detector_manager.add_detector)
        self.ui.check_box_active.stateChanged.connect(self.detector.toggle_active)
    # def add_detector(self):
    #     self.btn_add.setText('kk')

class DetectorManager:
    def __init__(self, detectors, btn_add, tab_widget, status_controller):
        self.detectors = detectors
        self.btn_add = btn_add
        self.tab_widget = tab_widget
        #self.tab = options_tab(self)
        self.set_events()
        self.status_controller = status_controller
        self.rect_colors = [(235, 10, 235), (240, 240, 10), (5, 240, 240), (5, 240, 240), (50, 40, 240), (50, 240, 140)]
        # self.add_detector()
        self.selected_name = None
        self.selected_conf_file = None
        # self.add_detector('HAAR Full Body', 'data/haarcascade_fullbody.xml')
        self.init_detectors()
    def set_events(self):
        self.btn_add.clicked.connect(self.add_detector)

    def init_detectors(self):
        self.selected_name = 'HAAR Full Body'
        self.selected_conf_file = 'data/haarcascade_fullbody.xml'
        self.add_detector( )
        self.selected_name = 'HAAR face'
        self.selected_conf_file = 'data/haarcascade_frontalface_alt.xml'
        self.add_detector( )
        self.selected_name = 'HAAR Full Body'
        self.selected_conf_file = 'data/haarcascade_fullbody.xml'

    def add_detector(self):
    # def add_detector(self):
        # https://stackoverflow.com/questions/68006651/pyqt5-how-to-addwidget-at-the-specific-position
        label = QLabel('')

        # self.detectors.append(detector.HAARcascades(name, config_file, self.rect_colors[len(self.detectors)],
        #                                             self.status_controller, label))
        #
        self.detectors.append(detector.HAARcascades(self.rect_colors[len(self.detectors)],
                                                    self.status_controller, label, self.selected_name, self.selected_conf_file))
        self.tab_widget.addTab(options_tab(self, self.detectors[-1]), f"{self.selected_name} {len(self.detectors )}")