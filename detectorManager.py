from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import detector
import uiOptionsTab

# use functools.partial to pass parameters when event is fired
# https://gis.stackexchange.com/questions/66616/connect-signal-to-function-with-arguments-python
from functools import partial


class OptionsTab(QWidget):
    def __init__(self, detector_manager, detector):
        super().__init__()
        self.ui = uiOptionsTab.Ui_Form()
        self.ui.setupUi(self)
        self.btn_add = self.ui.btn_add
        self.detector_manager = detector_manager
        self.detector = detector

        # TODO implement some save function for settings
        # self.ui.comboBox.addItem("Setting1")
        # self.ui.comboBox.addItem("Setting2")

        self.init_ui()
        self.set_events()
        self.q_color_dialog = QColorDialog()

    def init_ui(self):
        for prop in self.detector.tunable_params:
            hor_layout = QHBoxLayout()
            # self.ui.gridLayout.addLayout(hor_layout, -1,1)
            self.ui.verticalLayout.addLayout(hor_layout, -1)

            # self.ui.verticalLayout.insertLayout(-2, hor_layout)
            hor_layout.addWidget(QLabel(prop.name))
            if prop.type == "color":
                widget = QPushButton()
                hor_layout.addWidget(widget)

                widget.clicked.connect(partial(self.value_change, widget, prop, "color"))

            else:
                if prop.type == float:
                    widget = QDoubleSpinBox()
                else:
                    widget = QSpinBox()

                widget.setMinimum(prop.min_value)
                widget.setMaximum(prop.max_value)
                hor_layout.addWidget(widget)

                widget.valueChanged.connect(partial(self.value_change, widget, prop, "spin"))
        self.ui.verticalLayout.addStretch()
        # self.ui.gridLayout.a
    # https://stackoverflow.com/questions/940555/pyqt-sending-parameter-to-slot-when-connecting-to-a-signal
    # https://www.tutorialspoint.com/pyqt/pyqt_qspinbox_widget.htm
    def value_change(self, widget, prop, widget_type):
        if widget_type == "spin":
            prop.value = widget.value()
        # https://stackoverflow.com/questions/53690302/qcolordialoggetcolor-function-get-rgb-value-and-conver-to-hex
        if widget_type == "color":
            color = self.q_color_dialog.getColor()
            self.q_color_dialog.selectedColor = color
            q_rgb = color.rgb()
            rgb = (qBlue(q_rgb), qGreen(q_rgb), qRed(q_rgb))    # order swapped, just opencv things
            prop.value = rgb
            widget.setStyleSheet(f"background-color: rgb({rgb[2]}, {rgb[1]}, {rgb[0]});")

    def set_events(self):
        self.btn_add.clicked.connect(self.detector_manager.add_detector)
        self.ui.checkBox_active.stateChanged.connect(self.detector.toggle_active)


class DetectorManager:
    def __init__(self, tab_widget, wait4frame):
        self.detectors = []
        self.wait4frame = wait4frame
        # self.btn_add = btn_add
        self.tab_widget = tab_widget

        self.set_events()

        # TODO this will go horribly wrong
        self.rect_colors = [[235, 10, 235], [240, 240, 10], [5, 240, 240], [5, 240, 240], [50, 40, 240], [50, 240, 140]]

        self.selected_name = None
        self.selected_conf_file = None
        # self.add_detector('HAAR Full Body', 'data/haarcascade_fullbody.xml')
        self.init_detectors()

    def set_events(self):
        # self.btn_add.clicked.connect(self.add_detector)
        pass
    # TODO these should be loaded from ui
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
        # https://stackoverflow.com/questions/68006651/pyqt5-how-to-addwidget-at-the-specific-position
        label = QLabel('')
        self.detectors.append(detector.HAARCascades(self.rect_colors[len(self.detectors)],
                                                    label, self.selected_name, self.selected_conf_file))
        self.tab_widget.addTab(OptionsTab(self, self.detectors[-1]), f"{self.selected_name} {len(self.detectors)}")