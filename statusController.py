from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

class StatusController():

    def __init__(self, lay_delta_t):
        self.lay_delta_t = lay_delta_t
        # btn.clicked.connect(self.changeLabel)

    def changeLabel(self):
        #self.lbl.setText('this was changed by buttin')
        pass
    def show_duration(self):
        pass

    def add_detector(self, label):
        self.lay_delta_t.insertWidget(len(self.lay_delta_t) - 1, label)