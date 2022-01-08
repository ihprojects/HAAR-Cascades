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

        #add the item in combo box
        for item in items:
            self.cb.addItem(item)
        #define event, if index of combo box changed
        self.cb.currentIndexChanged.connect(self.selectionchange)

        return widget

    def selectionchange(self,selected_index):
        self._selectedIndex = selected_index
        self._selectedText = self.cb.currentText()







