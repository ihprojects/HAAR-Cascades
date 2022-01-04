from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import uiMainWindow
import videoPlayer
import detectorManager
import personCounter
import settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uiMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.wait4frame = QTimer(self)      # timer to fire time based event






        self.ui.tabWidget.removeTab(1)      # what
        self.ui.tabWidget.removeTab(0)      # ever
        self.detector_manager = detectorManager.DetectorManager( self.ui.tabWidget, self.wait4frame)

        self.video_player = videoPlayer.VideoPlayer(self.ui.btn_play_pause, self.ui.btn_stop, self.ui.lbl_video,
                                                    self.wait4frame, self.ui.sld_video)

        self.wait4frame.timeout.connect(self.run)
        self.show()

        self.input_menu = QMenu("Input")
        self.ui.menubar.addMenu(self.input_menu)
        self.select_video_file_action = QAction("Select File")
        self.cam_mode_action = QAction("Camera")
        self.cam_mode_action.setCheckable(True)
        self.file_mode_action = QAction("File")
        self.file_mode_action.setCheckable(True)

        self.input_menu.addActions([ self.cam_mode_action, self.file_mode_action])
        self.input_menu.addSeparator()
        self.input_menu.addAction(self.select_video_file_action)
        self.select_video_file_action.triggered.connect(self.action_triggered)
        self.cam_mode_action.triggered.connect(self.activate_cam_mode)
        self.file_mode_action.triggered.connect(self.activate_file_mode)


        #TODO this should be done from gui
        self.scenario = personCounter.PersonCounter(self.video_player)
        # self.scenario = personCounter.TestScenario()
        self.ui.lay_scenario.addWidget(self.scenario)
        self.file_mode_action.setChecked(True)
        self.activate_file_mode()


    def action_triggered(self):
        print("select File")

    def activate_cam_mode(self):
        # if self.cam_mode_action.isChecked():
        self.file_mode_action.setChecked(False)
        self.video_player.mode = "cam"
        self.video_player.load_video(0)
        self.scenario.init_ui()

    def activate_file_mode(self):
        # if self.file_mode_action.isChecked():
        self.cam_mode_action.setChecked(False)
        self.video_player.mode = "file"
        self.video_player.load_video(settings.DEFAULT_VIDEO_PATH)
        self.scenario.init_ui()

    def run(self):
        self.video_player.read_frame()

        for dtc in self.detector_manager.detectors:
            if dtc.is_active:
                dtc.get_rects(self.video_player.frame)
                self.scenario.process_frame(dtc)

        self.video_player.show_frame()


    # TODO add some hoykeys
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_K:
            self.video_player.play_pause()




