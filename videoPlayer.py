import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

import personCounter
import settings



class Video():
    def __init__(self, path, fps, total_frames):
        self.path = path
        self.fps = fps
        self.total_frames = total_frames

class VideoPlayer():
    def __init__(self, detectors, btn_play_pause, btn_stop, lbl_screen, lbl_fps, wait4frame, slider, scenario):
        self.video_path=settings.DEFAULT_VIDEO_PATH
        self.scenario = scenario
        self.detectors = detectors

        self.btn_play_pause = btn_play_pause
        self.btn_stop = btn_stop
        self.lbl_screen = lbl_screen
        self.lbl_fps = lbl_fps
        self.slider = slider
        self.frame = None

        self.is_playing = False
        self.video = None
        self.fps = 0
        self.fps_real = 0

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
        self.wait4frame.timeout.connect(self.get_frame)

    #this gets called by wait4frame timer event
    def get_frame(self):

        if 0 <= self.current_frame < self.video.total_frames:
            t1 = datetime.now()
            ret, self.frame = self.cap.read()
            self.current_frame += 1

            # get rects
            for dtc in self.detectors:
                if dtc.is_active:
                    dtc.get_rects(self.frame)
                    self.scenario.process_frame(self, dtc)

            # convert to img
            height, width, channel = self.frame.shape
            bytes_per_line = channel * width
            img = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

            # convert to pixmap
            pix_map = QPixmap(img)
            pix_map = pix_map.scaled(self.lbl_screen.width(), self.lbl_screen.height(),
                                   aspectRatioMode=Qt.KeepAspectRatio)  # wut?
            self.lbl_screen.setPixmap(pix_map)

            # https: // docs.python.org / 3 / library / datetime.html
            self.fps_real = int(-1/((self.t_1 - datetime.now()).total_seconds()))
            self.lbl_fps.setText(f"FPS: {str(self.fps_real)}")
            self.t_1 = datetime.now()
            self.current_frame += 1
            self.slider.setValue(self.current_frame)

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
        if self.cap is None:
            self.load_video(self.video_path)

        self.is_playing = True
        self.wait4frame.start(int((1 / self.fps) * 1000))
        self.btn_play_pause.setText("Pause")

    def stop(self):
        if self.cap:
            self.set_frame(1)
            self.wait4frame.stop()
            self.get_frame()
            self.is_playing = False
            self.btn_play_pause.setText("Play")

    def load_video(self, file_path):
        if settings.VIDEO_MODE == "cam":
            self.cap = cv2.VideoCapture(0)
            self.video = Video("Camera 1" ,30, 20000)
        else:
            self.cap = cv2.VideoCapture(file_path)
        # flag = 5 to get fps of video file ; flag = 7 to get n of all frames
            self.video = Video(file_path, round(self.cap.get(5)), self.cap.get(7))
        self.fps = self.video.fps
        self.slider.setRange(1, self.video.total_frames)

    def set_frame(self, frame_number):
        self.cap.set(1, frame_number)  # flag = 1 to set frame position # this drops fps

    def slider_moved(self):
        if self.cap is None:
            self.load_video(self.video_path)
        # https://www.tutorialspoint.com/pyqt/pyqt_qslider_widget_signal.htm
        # self.pause()
        self.current_frame = self.slider.sliderPosition()
        self.set_frame(self.current_frame)
        self.get_frame()
