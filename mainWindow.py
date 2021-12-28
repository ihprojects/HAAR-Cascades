from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import detector
import uiMainWindow
import statusController
import videoPlayer
import detectorManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uiMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.s_controller = statusController.StatusController(self.ui.lay_delta_t)
        # self.s_controller = statusController.StatusController(self.ui.widget_status.)

        self.wait4frame = QTimer(self)
        self.v_player = videoPlayer.VideoPlayer(self, self.ui.btn_play_pause,self.ui.btn_stop, self.ui.lbl_video,
                                                self.ui.lbl_fps, self.wait4frame,self.ui.sld_video)
        # self.ui.sld_video.setRange()

        # self.rect_colors = [(235, 10, 235), (240, 240, 10), (5, 240, 240)]

        self.detectors = []
        self.ui.tabWidget.removeTab(1)
        self.ui.tabWidget.removeTab(0)
        self.detectorManager = detectorManager.DetectorManager(self.detectors, self.ui.btn_add_detector, self.ui.tabWidget, self.s_controller)




        # self.add_detector('HAAR Full Body', 'data/haarcascade_fullbody.xml', self.ui.lay_delta_t)
        # self.add_detector('HAAR face', 'data/haarcascade_frontalface_alt.xml', self.ui.lay_delta_t)


        self.show()

    def add_detector(self, name, config_file, layout):
        #https://stackoverflow.com/questions/68006651/pyqt5-how-to-addwidget-at-the-specific-position
        label = QLabel('')
        layout.insertWidget(len(layout) -1 , label)
        self.detectors.append(detector.HAARcascades(name, config_file, self.rect_colors[len(self.detectors)],
                                                    self.s_controller, label))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_K:
            self.v_player.play_pause()




