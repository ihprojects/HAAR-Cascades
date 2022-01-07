from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


import videoPlayer
import detectorManager
import personCounter
import signals
 # use functools.partial to pass parameters when event is fired
# https://gis.stackexchange.com/questions/66616/connect-signal-to-function-with-arguments-python
from functools import partial



class MainWindow(QMainWindow):
    style_sheet_global = "background-color: rgb(70, 70, 70); color: rgb(209, 209, 209);"
    style_sheet_widgets = "background-color: rgb(52, 52, 52);"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Detector STUDIO")
        self.video_file = ""
        self.sigs = signals.Signals()
        # widgets
        self.detector_manager = detectorManager.DetectorManager(self.sigs)
        self.video_player = videoPlayer.VideoPlayer( self.sigs)
        self.scenario = personCounter.PersonCounter(self.video_player)


        self.init_ui()
        self.show()

    def init_ui(self):
        #set stylesheets
        self.setStyleSheet(self.style_sheet_global)
        self.detector_manager.setStyleSheet(self.style_sheet_widgets)
        self.video_player.setStyleSheet(self.style_sheet_widgets)
        self.scenario.setStyleSheet(self.style_sheet_widgets)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        #main window layout
        self.layout_main = QVBoxLayout(self.central_widget)
        self.layout_top_half = QHBoxLayout()
        self.layout_bottom_half = QHBoxLayout()
        self.layout_main.addLayout(self.layout_top_half)
        self.layout_main.addLayout(self.layout_bottom_half)

        self.layout_top_half.addWidget(self.video_player)
        self.layout_top_half.addWidget(self.detector_manager)
        self.layout_bottom_half.addWidget(self.scenario)

        #menubar
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.file_menu = QMenu("File")
        self.menubar.addMenu(self.file_menu)

        self.input_menu = QMenu("Input")
        self.select_video_file_action = QAction("OpenFile")
        self.cam_mode_action = QAction("Camera")
        self.file_mode_action = QAction("File")

        self.input_menu.addActions([self.cam_mode_action, self.file_mode_action])
        self.file_menu.addMenu(self.input_menu)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.select_video_file_action)


        #connect signals
        self.cam_mode_action.triggered.connect(self.activate_cam_mode)
        self.file_mode_action.triggered.connect(self.activate_file_mode)
        self.select_video_file_action.triggered.connect(self.open_video_file)
        self.sigs.pls_open_file.connect(self.open_video_file)

        self.sigs.wait4frame.timeout.connect(self.run)



    def run(self):
        self.video_player.read_frame()

        for dtc in self.detector_manager.get_detectors():
            if dtc.is_active:
                dtc.get_rects(self.video_player.frame)
                self.scenario.process_frame(dtc)

        self.video_player.show_frame()

    def activate_cam_mode(self):
        self.video_player.load_video(0, "cam")
        self.scenario.init_ui()
        self.video_player.play()

    def activate_file_mode(self):
        self.scenario.init_ui()
        if self.video_file == "":
            self.open_video_file()
        else:
            self.video_player.load_video(self.video_file, "file")
            self.video_player.play()

    def open_video_file(self):
        self.video_player.stop()
        self.video_file = QFileDialog.getOpenFileName(self, "Open file")[0]
        if self.video_file != "":
            self.video_player.load_video(self.video_file, "file")
            self.video_player.play()
            self.scenario.init_ui()

    # TODO add some hoykeys
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_K:
            self.video_player.play_pause()




