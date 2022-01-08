from PyQt5.QtWidgets import *
import pyqtgraph as pg
from PyQt5.QtCore import QDate
import datetime
import calendar
from PyQt5 import QtCore, QtGui, QtWidgets

# https://learndataanalysis.org/pyqt5-calendar-widget-example-for-beginners/
# https://stackoverflow.com/questions/59424546/python-pyqt5-qdateedit-get-date-string
#https://stackoverflow.com/questions/61449954/pyqt5-datepicker-popup


class MyDatePicker(QWidget):
    global currentYear, currentMonth

    currentMonth = datetime.datetime.now().month
    currentYear = datetime.datetime.now().year

    def __init__(self):
        super().__init__()
        self._selectedDate = "2022-01-01"


    def initUI(self,title):
        widget = QWidget()
        stackpanel = QHBoxLayout()
        widget.setLayout(stackpanel)

        self.calendar = QtWidgets.QDateEdit(calendarPopup=True)

        label = QLabel(title + " :")
        stackpanel.addWidget(label)
        stackpanel.addWidget(self.calendar)


        self.calendar.setMinimumDate(QDate(2022, 1, 1))
        self.calendar.setMaximumDate(
            QDate(currentYear, currentMonth + 1, calendar.monthrange(currentYear, currentMonth)[1]))

        #self.calendar.setSelectedDate(QDate(currentYear, currentMonth, 1))

        #self.calendar.clicked.connect(self.get_selected_Date)
        self.calendar.dateChanged.connect(self.get_selected_Date)

        return widget

    def get_selected_Date(self,qDate):
         self._selectedDate = f'{qDate.year()}-{qDate.month()}-{qDate.day()}'
         print(self._selectedDate)

