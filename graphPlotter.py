
import pyqtgraph as pg



class GraphPlotter():
    def __init__(self, target_layout):
        self.target_layout = target_layout
        self.graphWidget = pg.PlotWidget()
        target_layout.addWidget(self.graphWidget)
        self.y_axis_label = ""
        self.x_axis_label = ""
        self.title = ""

    def draw_graph(self, x_value, y_value):
        self.bar_graph = pg.BarGraphItem(x=x_value, height=y_value, width=0.5, brush='g', )
        self.target_layout.removeWidget(self.graphWidget)
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setLabel('left', self.y_axis_label, units ='sec')
        self.graphWidget.setLabel('bottom', self.x_axis_label, units='')
        self.graphWidget.addItem(self.bar_graph)
        self.target_layout.addWidget(self.graphWidget)

    def set_labels(self, title,y_label,x_label):
        self.title = title
        self.x_axis_label= x_label
        self.y_axis_label = y_label






