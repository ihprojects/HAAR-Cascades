from PyQt5.QtWidgets import *
import pyqtgraph as pg
from PyQt5.QtCore import QDate
import datetime
import calendar
from PyQt5 import QtCore, QtGui, QtWidgets


# https://learndataanalysis.org/pyqt5-calendar-widget-example-for-beginners/
# https://stackoverflow.com/questions/59424546/python-pyqt5-qdateedit-get-date-string
# https://stackoverflow.com/questions/61449954/pyqt5-datepicker-popup


class MyDatePicker(QWidget):
    global currentYear, currentMonth, currentDay

    currentMonth = datetime.datetime.now().month
    currentYear = datetime.datetime.now().year
    currentDay = datetime.datetime.now().day

    def __init__(self):
        super().__init__()
        self._selectedDate = "2022-01-01"

    def initUI(self, title):
        # Create a new widget
        widget = QWidget()
        # Create horizontal stack panel
        horizontal_stack = QHBoxLayout()
        # Bind horizontal stack panel on widget
        widget.setLayout(horizontal_stack)
        # Create a popup date picker
        self.calendar = QtWidgets.QDateEdit(calendarPopup=True)
        # Create a label widget
        label = QLabel(title + " :")
        # Add label and date picker widget to the horizontal stack
        horizontal_stack.addWidget(label)
        horizontal_stack.addWidget(self.calendar)
        # define a minimum date for the ui user
        self.calendar.setMinimumDate(QDate(2022, 1, 1))
        # define a minimum date for the ui user
        self.calendar.setMaximumDate(
            QDate(currentYear, currentMonth + 1, calendar.monthrange(currentYear, currentMonth)[1]))
        # predefine the displayed date on date picker
        self.calendar.setDate(QDate(currentYear, currentMonth, currentDay))
        # add date Change event
        self.calendar.dateChanged.connect(self.get_selected_Date)

        return widget

    def get_selected_Date(self, qDate):
        # select the
        self._selectedDate = f'{qDate.year()}-{qDate.month()}-{qDate.day()}'
