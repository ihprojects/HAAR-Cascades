# run this in terminal to convert mainWindow.ui
# pyuic5 -x mainWindow.ui -o uiMainWindow.py
# pyuic5 -x optionsTab.ui -o uiOptionsTab.py
# pyuic5 -x personCounter.ui -o uiPersonCounter.py


import sys
import mainWindow
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
# window = Window.Window(videopath)
window = mainWindow.MainWindow()
sys.exit(app.exec())


