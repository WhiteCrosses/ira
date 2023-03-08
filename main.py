import sys
import time

import numpy as np

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from scipy import signal
from scipy.fft import fftshift


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.sampleRate = 200
        self.freq = 1
        self.duration = 1
        
        self.x = np.linspace(0,self.duration, self.sampleRate * self.duration)
        self.N = self.sampleRate * self.duration
        
        #Set-up array holding pixel data
        self.imageArray = np.zeros((50,100))
        
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        wave_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        waterfall_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        
        
        
        
        layout.addWidget(wave_canvas)
        layout.addWidget(waterfall_canvas)
        #layout.addWidget()
        
        self._wave_ax = wave_canvas.figure.subplots()
        self._waterfall_ax = waterfall_canvas.figure.subplots()

        self.gnerateData()
        
        self._line = self._waterfall_ax.pcolormesh(np.reshape(self.imageArray,(50,100)),vmin=np.min(self.imageArray),vmax=np.max(self.imageArray), shading='gouraud')
        self._waterfall_ax.invert_yaxis()
        self._wave_ax.plot(0,0)
        self._wave_ax.autoscale(False)
        
        self._timer = waterfall_canvas.new_timer(50)
        self._timer.add_callback(self._update_canvas)
        self._timer.start()

    def _update_canvas(self):
        self.gnerateData()
        self._wave_ax.clear()
        x,y = self.checkPeaks()
        
        self._wave_ax.plot(self.freqArray,self.data)
        for i in x:
            self._wave_ax.axvline(x=i, color='r')
        
        self._line.set_array(np.reshape(self.imageArray,(50,100)))
        
        self._wave_ax.figure.canvas.draw()
        self._line.figure.canvas.draw()
    


    def gnerateData(self):
        rng = np.random.default_rng()
        #print(self.freq)
        displacement = np.random.rand() * 3
        self.freqArray = np.fft.rfftfreq(self.N, 1/self.sampleRate)
        self.signal = 3*np.sin(2*np.pi*self.freq*self.x)
        self.signal += np.sin(2*np.pi*4*self.x)
        self.signal += 0.5*np.sin(2*np.pi*7*self.x)
        
        self.data = np.fft.rfft(self.signal)

        #self.data - np.fft.fftshift(np.abs(self.data))
        #print(self.data)
        
        self.freq += 0.5
        self.data = np.abs(self.data)
        self.data = self.data[:-1]
        self.freqArray = self.freqArray[:-1]
        
        self.imageArray = np.roll(self.imageArray,1,axis=0)
        self.imageArray[0, :] = self.data
        
        
    def checkPeaks(self):
        x,y = signal.find_peaks(self.data)
        print((x,y))
        return x,y
        

if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()