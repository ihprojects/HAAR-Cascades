from PyQt5.QtWidgets import *
import pyqtgraph as pg
from PyQt5.QtCore import QDate
import datetime
import calendar
from PyQt5 import QtCore, QtGui, QtWidgets



class MyFrame(QWidget):

    def __init__(self):
        super().__init__()



    def initUI(self):
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setLineWidth(2.0)


        return frame


