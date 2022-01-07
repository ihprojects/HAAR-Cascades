from PyQt5.QtWidgets import *
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


#"Quelle: https://de.acervolima.com/pyqtgraph-hinzufugen-von-qt-widgets-mit-dem-balkendiagramm/"
# https://de.acervolima.com/einfuhrung-in-das-pyqtgraph-modul-in-python/

class Diagramm(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQtGraph")
        self.setGeometry(200, 200, 600, 500)
        self._xAxis = None
        self._yAxis = None
        self.is_plotted = False


    def UiComponents(self,x_value,y_value,x_Title,x_min =0, x_max =20,):
        self.widget = QWidget()
        plot = pg.plot()

        #Layout Properties
        plot.setXRange(x_min,x_max, padding=0)
        plot.showGrid(x=True, y=True)

        #plot.addLegend()
        plot.setLabel('left', 'looking time', units='sec')
        plot.setLabel('bottom', x_Title, units='')
        self.bargraph = pg.BarGraphItem(x=x_value , height=y_value,width=0.5 ,brush='g',)
        plot.addItem(self.bargraph)
        layout = QGridLayout()
        self.widget.setLayout(layout)
        layout.addWidget(plot)
        self.setCentralWidget(self.widget)

        return self.widget

    def update_plot_data(self):
        self.bargraph.update()










