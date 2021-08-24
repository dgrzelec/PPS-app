import sys
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker

import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PPSclass import PPS
from PyQt5.QtCore import pyqtSlot

class ScatterCanvas(FigureCanvas):
    def __init__(self, parent=None, width=6, height=6, dpi=100):
        # plt.rcParams.update({
        #     "lines.color": "black",
        #     "patch.edgecolor": "black",
        #     "text.color": "black",
        #     "axes.facecolor": "black",
        #     "axes.edgecolor": "black",
        #     "axes.labelcolor": "black",
        #     "xtick.color": "black",
        #     "ytick.color": "black",
        #     "grid.color": "black",
        #     "figure.facecolor": "black",
        #     "figure.edgecolor": "black",
        #     "savefig.facecolor": "black",
        #     "savefig.edgecolor": "black"})

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.axes.xaxis.set_major_locator(plt.NullLocator())
        self.axes.yaxis.set_major_locator(plt.NullLocator())

        super(ScatterCanvas, self).__init__(fig)
        fig.tight_layout()

class PPS_APP(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('window_layout_2v2.ui', self)
        #canvas
        self.canvas = ScatterCanvas(self, width=12, height=12, dpi=100)
        self.ui.okno_grid_2.addWidget(self.canvas, 2,0,1,0)

        self.resize(1100, 700)

        self.interval = 100
        self.interval_pb = 10

        #model parameters
        self.r = 5
        self.alpha = np.pi
        self.beta = 17/180*np.pi
        self.v = 0.67
        self.PPS = PPS(self.r, self.alpha, self.beta, self.v)

        self.W = self.width_slid.value()
        self.H = self.height_slid.value()
        self.update_height_label(self.H)
        self.update_width_label(self.W)

        self.R = 5
        self.radius_slider.setValue(self.R)
        self.update_radius_value_label(self.R)

        self.N = 0
        self.method = 'random'
        self.density = 0

        self.a = 5

        self.method_list.setCurrentText(self.method)
        self.a_lbl.setVisible(False)
        self.a_value.setVisible(False)

        self.a_value.setValue(self.a)

        self.density_btn.setChecked(True)
        self.start_density = 0.08
        self.particle_value.setValue(self.start_density)


        self.area_update()
        #plot t=0 data
        self.dataX = []
        self.dataY = []

        #other initializations
        self.progress_update()

        self.timer_ani = QtCore.QTimer()
        self.timer_ani.setInterval(self.interval)  # msec
        #self.timer_ani.timeout.connect(self.update_plot) #TO DO

        self.timer_progress = QtCore.QTimer()
        self.timer_progress.setInterval(self.interval_pb)
        self.timer_progress.timeout.connect(self.progress_update)


        #threads init
        self.threadpool = QtCore.QThreadPool()

        #connections
        self.width_slid.valueChanged.connect(self.update_width_label)
        self.height_slid.valueChanged.connect(self.update_height_label)
        self.width_slid.sliderReleased.connect(self.width_slid_released)
        self.height_slid.sliderReleased.connect(self.height_slid_released)

        self.radius_slider.valueChanged.connect(self.update_radius_value_label)

        self.run_btn.clicked.connect(self.run_clicked)

        self.method_list.currentTextChanged.connect(self.method_changed)



    def width_slid_released(self):
        pass

    def height_slid_released(self):
        pass

    def a_relationships(self):
        if self.H < self.W:
            self.a_value.setMaximum(self.H)
        else:
            self.a_value.setMaximum(self.W)

    def method_changed(self, text):
        self.method = text
        if text == "random":
            self.a_lbl.setVisible(False)
            self.a_value.setVisible(False)
        elif text == "center":
            self.a_lbl.setVisible(True)
            self.a_value.setVisible(True)

    def run_clicked(self):

        self.width_slid.setEnabled(False)
        self.height_slid.setEnabled(False)
        self.density_btn.setEnabled(False)
        self.quantity_btn.setEnabled(False)
        self.method_list.setEnabled(False)
        self.particle_value.setEnabled(False)
        self.a_value.setEnabled(False) #dodaj tutej model ->> ZROBIONE :3
        self.radius_slider.setEnabled(False)
        self.alpha_value.setEnabled(False)
        self.beta_value.setEnabled(False)
        self.velocity_value.setEnabled(False)
        self.save_modified.setEnabled(False)


    def progress_update(self):
        value = self.PPS.get_progress()
        self.progress_bar.setValue(value)

    def model_update(self): #not working now
        # PPSclass object init
        self.PPS = PPS(self.r, self.alpha, self.beta, self.v)

    def area_update(self):
        self.PPS.area_init(self.W, self.H)

    def update_width_label(self, value):
        self.width_value_label.setText(str(value))
        self.W = self.width_slid.value()
        self.area_update()

    def update_height_label(self, value):
        self.height_value_label.setText(str(value))
        self.H = self.height_slid.value()
        self.area_update()

    def update_radius_value_label(self, value):
        self.radius_value_label.setText(str(value))
        self.R = self.radius_slider.value()



class Worker(QtCore.QRunnable):

    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.function(*self.args, **self.kwargs)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = PPS_APP()
    mainWindow.show()
    sys.exit(app.exec_())