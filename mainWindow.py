from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import uiMainWindow
import videoPlayer
import detectorManager
import personCounter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uiMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.wait4frame = QTimer(self)      # timer to fire time based event

        #TODO this should be done from gui
        self.scenario = personCounter.PersonCounter()
        # self.scenario = personCounter.TestScenario()


        self.ui.lay_scenario.addWidget(self.scenario)

        self.ui.tabWidget.removeTab(1)      # what
        self.ui.tabWidget.removeTab(0)      # ever
        self.detector_manager = detectorManager.DetectorManager( self.ui.tabWidget, self.wait4frame)

        self.video_player = videoPlayer.VideoPlayer(self.detector_manager.detectors, self.ui.btn_play_pause,
                                                    self.ui.btn_stop, self.ui.lbl_video,
                                                    self.ui.lbl_fps, self.wait4frame, self.ui.sld_video, self.scenario)





        self.show()


    # TODO add some hoykeys
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_K:
            self.video_player.play_pause()




