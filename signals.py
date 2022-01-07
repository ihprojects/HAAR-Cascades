from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# custom signals
class Signals(QObject):
    pls_pause = pyqtSignal()  # must be done outside of constructor: https://coderedirect.com/questions/318779/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect
    pls_resume = pyqtSignal()
    pls_open_file = pyqtSignal()

    # timer to fire time based event
    wait4frame = QTimer()

    def __init__(self):
        super().__init__()
        pass