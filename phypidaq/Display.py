# -*- coding: utf-8 -*-

'''Class providing graphical display and, optionally, a control interface
'''

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np, time, sys
import multiprocessing as mp

import matplotlib
from PyQt5 import QtWidgets
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt, matplotlib.animation as anim


class DisplayDataThread(QtCore.QThread):

    # Define all slots for new data
    new_data = QtCore.pyqtSignal(int, np.ndarray)
    lagging_update = QtCore.pyqtSignal(bool)

    def __init__(self, interval: int, data_queue, parent=None):
        super(DisplayDataThread, self).__init__(parent)
        self.interval = interval
        self.data_queue = data_queue

        # TODO: Check if data queue is set

    def run(self) -> None:
        count = 0
        lagging = False
        last_time = time.time()

        while True:
            if not self.data_queue.empty():
                data = self.data_queue.get()
                if type(data) != np.ndarray:
                    # Stop the thread
                    break
                count += 1
                # Send the received data to the UI
                self.new_data.emit(count, data)

            current_time = time.time()
            delta_time = current_time - last_time

            if delta_time - self.interval < self.interval * 0.01:
                if lagging:
                    lagging = False
                    # Send the update only once
                    self.lagging_update.emit(lagging)
            else:
                if not lagging:
                    lagging = True
                    # Send the update only once
                    self.lagging_update.emit(lagging)

            # Update the time for the lagging analysis
            last_time = current_time


class Display(QMainWindow):
    '''configure and control graphical data displays'''

    def __init__(self, interval=0.1, confdict=None, cmdQ=None, datQ=None):
        '''Args:
             interval:  logging interval, eventually overwritten by entry in confdict
             confdict:  dictionary with configuration
             cmdQ:      multiprocessing Queue for command transfer to caller
             datQ:      multiprocessing Queue for data transfer
        '''

        super().__init__()
        self.setWindowTitle("PhyPiDAQ Display")
        self.setMinimumSize(500, 300)

        # Center the window on the window
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)



        #self._dynamic_ax = dynamic_canvas.figure.subplots()
        #t = np.linspace(0, 10, 101)
        # Set up a Line2D.
        #self._line, = self._dynamic_ax.plot(t, np.sin(t + time.time()))

        #
        #dynamic_canvas.draw()

        self.cmdQ = cmdQ
        self.datQ = datQ
        if confdict != None:
            self.confdict = confdict
        else:
            self.confdict = {}

        # set default options for graphical display
        if 'Interval' not in self.confdict:
            self.confdict['Interval'] = interval
        else:
            interval = self.confdict['Interval']
        if interval < 0.05:
            print(" !!! read-out intervals < 0.05 s not reliable, setting to 0.05 s")
            self.confdict['Interval'] = 0.05

        if 'XYmode' not in self.confdict:  # default is XY mode off
            self.confdict['XYmode'] = False

        if 'DisplayModule' not in self.confdict:  # default display is DataLogger
            self.confdict['DisplayModule'] = 'DataLogger'

        if 'startActive' not in self.confdict:  # default is to start in Paused mode
            self.confdict['startActive'] = False

        # set channel properties
        if 'NChannels' not in self.confdict:
            self.confdict['NChannels'] = 1

        NC = self.confdict['NChannels']
        if 'ChanLimits' not in self.confdict:
            self.confdict['ChanLimits'] = [[0., 5.]] * NC
        if 'ChanNams' not in self.confdict:
            self.confdict['ChanNams'] = [''] * NC
        if 'ChanUnits' not in self.confdict:
            self.confdict['ChanUnits'] = ['V'] * NC

        if 'ChanLabels' not in self.confdict:
            self.confdict['ChanLabesl'] = [''] * NC

        # set display control options
        if 'startActive' not in self.confdict:  # start with active data taking
            self.self.confdict['startActive'] = True

        if 'DAQCntrl' not in self.confdict:  # no run control buttons
            self.confdict['DAQCntrl'] = False

        ModuleName = self.confdict['DisplayModule']  # name of the display module

        # TODO: Check if there are safer ways for doing this
        # import relevant library
        try:
            cmnd = 'from .' + ModuleName + ' import *'
            exec(cmnd, globals(), locals())
        except Exception as e:
            print(' !!! Display: failed to import module - exiting')
            print(str(e))
            sys.exit(1)

        try:
            cmnd = 'global DG; DG = ' + ModuleName + '(self.confdict)'
            exec(cmnd, globals(), locals())
        except Exception as e:
            print(' !!! Display: failed to initialize module - exiting')
            print(str(e))
            sys.exit(1)

        # Init the
        DG.init()

        dynamic_canvas = FigureCanvas(DG.fig)
        layout.addWidget(dynamic_canvas)

        def yieldEvt_fromQ():
            # receive data via a Queue from package multiprocessing
            cnt = 0

            while True:
                if not self.datQ.empty():
                    data = self.datQ.get()
                    print(cnt)
                    if type(data) != np.ndarray:
                        break  # received end event
                    cnt += 1
                    yield (cnt, data)
                else:
                    yield None  # send empty event if no new data

            # end of yieldEvt_fromQ
            sys.exit()

        self.animation = anim.FuncAnimation(DG.fig, DG, yieldEvt_fromQ, interval=50, repeat=True, blit=True)

    def _update_canvas(self, i):
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._line.set_data(t, np.sin(t + time.time()))
        return self._line,

    def init(self):
        '''create data transfer queue and start display process'''

        if self.datQ == None:
            self.datQ = mp.Queue(1)  # Queue for data transfer to sub-process
        DisplayModule = self.confdict['DisplayModule']

    def showData(self, dat):
        # send data to display process
        print("New data!")
        self.datQ.put(dat)
        time.sleep(0.00005)  # !!! waiting time to make data transfer reliable

    def closeDisplay(self):
        self.close()
