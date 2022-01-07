import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Video():
    def __init__(self, name, fps, total_frames):
        self.name = name
        self.fps = fps
        self.total_frames = total_frames

class VideoPlayer(QWidget):
    def __init__(self, wait4frame, pls_open_file):
        super().__init__()
        self.frame = None
        self.is_playing = False
        self.video = None
        self.is_ready = False
        self.fps = 30
        self.screen_size = (1920, 1080)     #default screen size
        self.read_frame = self.read_frame_from_file
        self.current_frame = 1

        self.wait4frame = wait4frame
        self.open_file = pls_open_file
        self.cap = None
        self.init_ui()

    def init_ui(self):
        self.layout_main = QVBoxLayout(self)

        #screen
        self.screen = QLabel()
        self.screen.setMinimumSize(QSize(800, 450))
        self.screen.setMaximumSize(QSize(800, 450))


        #buttons
        self.layout_buttons = QHBoxLayout()
        self.btn_play_pause = QPushButton()
        self.btn_play_pause.setText("Play")
        self.btn_stop = QPushButton()
        self.btn_stop.setText("Stop")
        self.layout_buttons.addWidget(self.btn_play_pause)
        self.layout_buttons.addWidget(self.btn_stop)
        self.layout_buttons.addStretch()

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)


        self.layout_main.addWidget(self.screen)
        self.layout_main.addWidget(self.slider)
        self.layout_main.addLayout(self.layout_buttons)


        #connect signals
        self.btn_play_pause.clicked.connect(self.play_pause)
        self.btn_stop.clicked.connect(self.stop)
        self.slider.sliderPressed.connect(self.pause)
        self.slider.sliderReleased.connect(self.set_frame)



    def play_pause(self):
        if self.is_playing:
            self.pause()
        else:
            self.play()

    def pause(self):
        self.is_playing = False
        self.wait4frame.stop()
        self.btn_play_pause.setText("Play")

    def play(self):
        if self.is_ready:
            self.is_playing = True
            self.wait4frame.start(int((1 / self.fps) * 1000))
            self.btn_play_pause.setText("Pause")
        else:
            self.open_file.emit()
    def stop(self):
        if self.cap:
            self.slider.setValue(0)
            self.set_frame()
            self.wait4frame.stop()
            self.is_playing = False
            self.btn_play_pause.setText("Play")

    def load_video(self, input_type, mode):
        if mode == "cam":
            self.cap = cv2.VideoCapture(input_type)
            self.read_frame = self.read_frame_from_cam
            self.slider.hide()
            self.fps = 30
            self.read_frame()
            self.screen_size = (self.frame.shape[1], self.frame.shape[0])
            self.is_ready = True
        if mode == "file":

            self.cap = cv2.VideoCapture(input_type)

            self.read_frame= self.read_frame_from_file
            # flag = 5 to get fps of video file ; flag = 7 to get n of all frames
            self.video = Video(input_type, round(self.cap.get(5)), self.cap.get(7))
            self.fps = self.video.fps
            self.slider.show()
            self.slider.setRange(1, self.video.total_frames)

            self.read_frame()
            self.screen_size = (self.frame.shape[1], self.frame.shape[0])
            self.is_ready = True


    def set_frame(self):
        # https://www.tutorialspoint.com/pyqt/pyqt_qslider_widget_signal.htm
        self.pause()
        self.current_frame = self.slider.sliderPosition()
        self.cap.set(1, self.current_frame)  # flag = 1 to set frame position
        self.read_frame()
        self.show_frame()


    def read_frame_from_file(self):
        if 0 <= self.current_frame < self.video.total_frames:
            ret, self.frame = self.cap.read()
            self.current_frame += 1
            self.slider.setValue(self.slider.value()+1)

    def read_frame_from_cam(self):
        ret, self.frame = self.cap.read()


    def show_frame(self):
        # convert to img
        height, width, channel = self.frame.shape
        bytes_per_line = channel * width
        img = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

        # convert to pixmap
        pix_map = QPixmap(img)
        pix_map = pix_map.scaled(self.screen.width(), self.screen.height())
        self.screen.setPixmap(pix_map)

