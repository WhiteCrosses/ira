import sys
import matplotlib

matplotlib.use('qtagg')

from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import QApplication, QSizePolicy, QGroupBox, QSlider, QWidget, QLabel, QDesktopWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.fft import fftshift
from PyQt5.QtGui import QColor, QPainter
from waterfallplot import WaterfallPlot
from pyqtspecgram import pyqtspecgram

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        print("entered init")
        self.x_vals = np.linspace(0, 10, 100)
        screen = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen.width(), screen.height()

        #calculate center position of the screen for the window
        window_width, window_height = 800,600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.data = np.zeros(5000)
        self.data = self.data.reshape((50,100))
        hbox = QHBoxLayout()

        leftBox = self.leftBox()
        midBox = self.middleBox()

        hbox.addWidget(leftBox)
        hbox.addWidget(midBox)
        
        self.setLayout(hbox)
        
        self.setGeometry(x, y, window_width, window_height)
        self.setWindowTitle('My PyQt5 App')
        self.setStyleSheet('background-color: #ffffff')
        #self.setStyleSheet('background-color: #041014')
        

        self.show()


    def leftBox(self):

        box = QGroupBox("Left Box")
        layout = QVBoxLayout()
        slider1 = QSlider(Qt.Horizontal)
        slider2 = QSlider(Qt.Horizontal)
        slider3 = QSlider(Qt.Horizontal)
        slider4 = QSlider(Qt.Horizontal)
        layout.addWidget(slider1)
        layout.addWidget(slider2)
        layout.addWidget(slider3)
        layout.addWidget(slider4)

        box.setLayout(layout)
        
        return box


    def middleBox(self):
        box = QGroupBox("Middle Box")
        layout = QVBoxLayout()

        plot = self.plotBox()
        layout.addWidget(plot)
        
        box.setLayout(layout)
        return box


    def plotBox(self):
        widget = QWidget()
        layout = QVBoxLayout()
        wavePlot = self.wavePlot()
        #self.waterfall_plot = QWidget()
        
        self.waterfall_fig = Figure()
        self.waterfall_plot = self.waterfall_fig.add_subplot()
        #self.waterfall_pixmap = self.waterfall_plot.update(self.waterfall_plot, self.data, self.x_vals)
        self.waterfall_canvas = FigureCanvas(self.waterfall_fig)
        #layout.addWidget(wavePlot)
        layout.addWidget(self.waterfall_canvas)

        widget.setLayout(layout)

        self._timer = QTimer()
        self._timer.timeout.connect(self.updatePlot)
        self._timer.start(1000)

        return widget


    def wavePlot(self):

        # Create a vertical layout for the widget
        layout = QVBoxLayout()
        widget = QWidget()
        
        # Create a new figure and add a subplot to it
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        #self.canvas = FigureCanvas(fig)

        
        self.y_vals = self.stacked_sine(5,[1, 500],[0, np.pi],[0.5, 1.5],self.x_vals)

        fft_vals = self.calculate_fft(self.y_vals)

        fig.clear()
        self.ax = fig.add_subplot(111)
        freq_range = np.linspace(0, 100, fft_vals.size//2)
        self.ax.plot(freq_range,np.abs(fft_vals[:fft_vals.size//2]))
        
        return self.canvas


    def stacked_sine(self,num_sines, freq_range, phase_range, amp_range, x_vals):
        """
        Generates a stack of sine waves with random frequency, phase, and amplitude.

        Args:
            num_sines (int): The number of sine waves to generate.
            freq_range (tuple): A tuple (min_freq, max_freq) representing the range of frequencies
                for the sine waves. Frequencies are generated randomly within this range.
            phase_range (tuple): A tuple (min_phase, max_phase) representing the range of phases
                for the sine waves. Phases are generated randomly within this range.
            amp_range (tuple): A tuple (min_amp, max_amp) representing the range of amplitudes
                for the sine waves. Amplitudes are generated randomly within this range.
            x_vals (ndarray): An array of x values at which to calculate the stacked sine waves.

        Returns:
            An ndarray of the same shape as x_vals containing the values of the stacked sine waves.
        """
        y_vals = np.zeros_like(x_vals)

        for i in range(num_sines):
            freq = np.random.uniform(freq_range[0], freq_range[1])
            phase = np.random.uniform(phase_range[0], phase_range[1])
            amp = np.random.uniform(amp_range[0], amp_range[1])
            y_vals += amp * np.sin(2*np.pi*freq*x_vals + phase)

        return y_vals


    def calculate_fft(self,input_array):
        """
        Calculates the FFT of the input array.

        Args:
            input_array (ndarray): An array of input values.

        Returns:
            An ndarray of FFT values corresponding to the input array.
        """
        fft_vals = np.fft.fft(input_array)
        return fft_vals

    def updateArray(self, array):

        new_row = np.zeros((np.size(self.x_vals)))
        self.data = np.roll(self.data,1,axis=0)
        self.data = self.data.reshape(50,100)
        print(type(array))
        print(type(self.data))
        print(np.size(self.data))
        self.data[0, :] = array
        #self.data = self.data[:-1, :]

    def generateWaterfall(self):
        return 0
    
    def updatePlot(self):
        
        print("Update Caalled")
        y_vals = self.stacked_sine(5,[1, 500],[0, np.pi],[0.5, 1.5],self.x_vals)
        fft_vals = self.calculate_fft(y_vals)
        self.updateArray(fft_vals)

        freq_range = np.linspace(0, 100, fft_vals.size//2)
        self.ax.clear()
        self.ax.plot(freq_range,np.abs(fft_vals[:fft_vals.size//2]))
        #self.canvas.draw()

        fft_freq = np.fft.fftfreq(self.data.shape[-1])
        idx = np.argsort(fft_freq)
        self.waterfall_widget = self.waterfall_plot.update(self.waterfall_plot,self.data, self.x_vals)

        f,t,Sxx = signal.spectrogram(fft_vals, 0.001)
        self.waterfall_plot.pcolormesh(f, t, np.transpose(Sxx), shading='gouraud')
        


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
