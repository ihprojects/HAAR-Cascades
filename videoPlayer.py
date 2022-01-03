import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

import personCounter
import settings



class Video():
    def __init__(self, name, fps, total_frames):
        self.name = name
        self.fps = fps
        self.total_frames = total_frames

class VideoPlayer():
    def __init__(self, btn_play_pause, btn_stop, lbl_screen, wait4frame, slider):
        self.video_path= None

        self.btn_play_pause = btn_play_pause
        self.btn_stop = btn_stop
        self.lbl_screen = lbl_screen
        self.slider = slider
        self.frame = None

        self.is_playing = False
        self.video = None
        self.fps = 0
        self.fps_real = 0
        self.screen_size = (1920, 1080)     #default screen size
        self.mode = "file"
        self.current_frame = 1

        # self.wait4frame = QTimer(main_win)
        self.wait4frame = wait4frame

        self.cap = None
        self.set_events()
        self.frame_np = None

        self.t_1 = datetime.now()
    def set_events(self):
        self.btn_play_pause.clicked.connect(self.play_pause)
        self.btn_stop.clicked.connect(self.stop)
        self.slider.sliderPressed.connect(self.pause)
        self.slider.sliderReleased.connect(self.slider_moved)
        # self.wait4frame.timeout.connect(self.get_frame)


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
        self.is_playing = True
        self.wait4frame.start(int((1 / self.fps) * 1000))
        self.btn_play_pause.setText("Pause")

    def stop(self):
        if self.cap:
            self.set_frame(1)
            self.wait4frame.stop()
            self.is_playing = False
            self.btn_play_pause.setText("Play")

    def load_video(self, file_path):
        self.cap = cv2.VideoCapture(file_path)
        if self.mode == "cam":

            self.video = Video("Camera 1" ,30, 20000)
        else:

        # flag = 5 to get fps of video file ; flag = 7 to get n of all frames
            self.video = Video(file_path, round(self.cap.get(5)), self.cap.get(7))




        self.fps = self.video.fps
        self.read_frame()
        self.slider.setRange(1, self.video.total_frames)
        self.screen_size = (self.frame.shape[1], self.frame.shape[0])

    def set_frame(self, frame_number):
        self.cap.set(1, frame_number)  # flag = 1 to set frame position # this drops fps

    def slider_moved(self):
        # https://www.tutorialspoint.com/pyqt/pyqt_qslider_widget_signal.htm
        self.pause()
        self.current_frame = self.slider.sliderPosition()
        self.set_frame(self.current_frame)

        self.read_frame()
        self.show_frame()

    def read_frame(self):

        if 0 <= self.current_frame < self.video.total_frames:
            ret, self.frame = self.cap.read()
            self.current_frame += 1

    def show_frame(self):
        # convert to img
        height, width, channel = self.frame.shape
        bytes_per_line = channel * width
        img = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

        # convert to pixmap
        pix_map = QPixmap(img)
        pix_map = pix_map.scaled(self.lbl_screen.width(), self.lbl_screen.height())
        self.lbl_screen.setPixmap(pix_map)