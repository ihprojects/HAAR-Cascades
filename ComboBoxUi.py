from PyQt5.QtWidgets import *
import pyqtgraph as pg
from PyQt5.QtCore import QDate
import datetime
import calendar
from PyQt5 import QtCore, QtGui, QtWidgets


class MyCombobox(QWidget):
    def __init__(self):
        super().__init__()
        self._selectedIndex =0;
        self._selectedText = None



    def initUI(self,items,title):
        widget = QWidget()
        stackpanel = QHBoxLayout()
        widget.setLayout(stackpanel)

        self.cb = QComboBox()
        label = QLabel(title+" :")
        stackpanel.addWidget(label)
        stackpanel.addWidget(self.cb)

        for item in items:
            self.cb.addItem(item)

        self.cb.currentIndexChanged.connect(self.selectionchange)

        return widget

    def selectionchange(self,i):
        self._selectedIndex = i
        self._selectedText = self.cb.currentText()







