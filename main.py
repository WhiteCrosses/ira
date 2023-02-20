from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import QTimer
import sys
import gui
import time

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import numpy as np
        

class MainWidget(QWidget, gui.Ui_MainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.setupUi(self)

        self.layout = QVBoxLayout(self)
        self.spectra = self.layout.addWidget(SpectraWidget())


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        ax = self.figure.add_gridspec(2,1)
        self.wave_axis = self.figure.add_subplot(ax[0,0])
        self.axis = self.figure.add_subplot(ax[1,0])
        self.figure.subplots_adjust(bottom=0.1, right=0.5, top=0.9)
        self.layoutvertical = QVBoxLayout(self)
        self.layoutvertical.addWidget(self.canvas)

class SpectraWidget(QWidget):
    def __init__(self):
        super(SpectraWidget, self).__init__()
        #self.setupUi(self)
        self.setStyleSheet("background-color: green;")
        self.init_widget()
        self.plot_widget()
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start()
        

    def init_widget(self):
        self.matplotlibwidget = MatplotlibWidget()
        self.matplotlibwidget.axis.set_axis_off()
        self.layoutvertical = QVBoxLayout(self)
        self.layoutvertical.addWidget(self.matplotlibwidget)

    def timerEvent(self):
        self.Z = np.sin(time.time() + self.Y) * np.sin(self.X)
        self.cax.set_data(self.Z)
        self.z = np.sin(time.time()) * np.sin(self.x)
        self.matplotlibwidget.wave_axis.clear()
        self.matplotlibwidget.wave_axis.plot(self.x,self.z)
        self.matplotlibwidget.wave_axis.plot(1)
        self.matplotlibwidget.wave_axis.plot(-1)
        self.matplotlibwidget.canvas.draw()

    def plot_widget(self):
        self.matplotlibwidget.axis.clear()
        self.x = np.linspace(0, 20, 20)
        self.y = np.linspace(0, 6, 60)
        self.z = np.sin(self.x)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.Z = np.sin(self.X)

        self.cax = self.matplotlibwidget.axis.imshow(self.Z, cmap='viridis', extent=[0,20,0,6])
        #self.cax.axes.set_xlim(0,10)
        self.cax_wave = self.matplotlibwidget.wave_axis.plot(self.x,self.z)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWidget()
    
    w.show()
    sys.exit(app.exec_())

