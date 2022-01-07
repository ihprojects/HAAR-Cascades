import sys
from PyQt5.QtWidgets import (QLabel, QRadioButton,
                             QPushButton, QVBoxLayout,
                             QApplication, QWidget,
                             QButtonGroup)


#Quelle: https://www.delftstack.com/de/tutorial/pyqt5/pyqt5-radiobutton/

class MyRadiobutton(QWidget):

    def __init__(self):
        super().__init__()
        self.label = QLabel('Select Layout')
        self.rbtn1 = QRadioButton('Layout 1')
        self.rbtn1.setChecked(True)

        self.rbtn2 = QRadioButton('Layout 2')
        self.rbtn3 = QRadioButton('Layout 3')
        self.rbtn4 = QRadioButton('All')

    def init_ui(self):
        self.btngroup1 = QButtonGroup()
        #self.btngroup2 = QButtonGroup()

        self.btngroup1.addButton(self.rbtn1)
        self.btngroup1.addButton(self.rbtn2)
        self.btngroup1.addButton(self.rbtn3)
        self.btngroup1.addButton(self.rbtn4)

        self.rbtn1.toggled.connect(self.onClickedCity)
        self.rbtn2.toggled.connect(self.onClickedCity)

        self.rbtn3.toggled.connect(self.onClickedCity)
        self.rbtn4.toggled.connect(self.onClickedCity)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.rbtn1)
        layout.addWidget(self.rbtn2)
        #layout.addWidget(self.label2)

        #layout.addWidget(self.label3)
        layout.addWidget(self.rbtn3)
        layout.addWidget(self.rbtn4)
       # layout.addWidget(self.label4)

        self.setGeometry(200, 200, 300, 300)
        self.setLayout(layout)


        return layout
        #self.setWindowTitle('PyQt5 Radio Button Example')



    def onClickedCity(self):
        radio_btn = self.sender()

        '''if radio_btn.isChecked():
            self.label2.setText("You live in " + radio_btn.text())'''

    def onClickedState(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.label4.setText("You live in " + radioBtn.text())
