#run this to convert win ui
#pyuic5 -x win.ui -o win.py
#pyuic5 -x mainWindow.ui -o uiMainWindow.py



import sys

import mainWindow
from PyQt5.QtWidgets import *







app = QApplication(sys.argv)
# window = Window.Window(videopath)
window = mainWindow.MainWindow()
sys.exit(app.exec())


