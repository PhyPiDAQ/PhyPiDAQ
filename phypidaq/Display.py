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

from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QPushButton
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt, matplotlib.animation as anim


class Display(QMainWindow):
    """
    QWidget to display a dynamic matplotlib.pyplot in it
    """

    def __init__(self, interval=0.1, config_dict=None, cmd_queue=None, data_queue=None):
        """
        :argument:
             interval:    logging interval, eventually overwritten by entry in config_dict
             config_dict: dictionary with configuration
             cmd_queue:   multiprocessing Queue for command transfer to caller
             data_queue:  multiprocessing Queue for data transfer
        """

        # Setup a basic window
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
        button_layout = QtWidgets.QHBoxLayout()

        # Setup configuration
        self.cmd_queue = cmd_queue

        # Check if the data_queue is initialised and create one, if it is none
        if data_queue is None:
            self.data_queue = mp.Queue(1)
        else:
            self.data_queue = data_queue

        if config_dict is not None:
            self.config_dict = config_dict
        else:
            self.config_dict = {}

        # Set default options for graphical display
        if 'Interval' not in self.config_dict:
            self.config_dict['Interval'] = interval
        else:
            interval = self.config_dict['Interval']
        if interval < 0.05:
            print(" !!! read-out intervals < 0.05 s not reliable, setting to 0.05 s")
            self.config_dict['Interval'] = 0.05

        # XY mode is by default off
        if 'XYmode' not in self.config_dict:
            self.config_dict['XYmode'] = False

        # The default display is DataLogger
        if 'DisplayModule' not in self.config_dict:
            self.config_dict['DisplayModule'] = 'DataLogger'

        # Default mode is started
        if 'startActive' not in self.config_dict:
            self.config_dict['startActive'] = True

        # No run control buttons by default
        if 'DAQCntrl' not in self.config_dict:
            self.config_dict['DAQCntrl'] = False

        # Set channel properties
        if 'NChannels' not in self.config_dict:
            self.config_dict['NChannels'] = 1

        NC = self.config_dict['NChannels']
        if 'ChanLimits' not in self.config_dict:
            self.config_dict['ChanLimits'] = [[0., 5.]] * NC
        if 'ChanNams' not in self.config_dict:
            self.config_dict['ChanNams'] = [''] * NC
        if 'ChanUnits' not in self.config_dict:
            self.config_dict['ChanUnits'] = ['V'] * NC

        if 'ChanLabels' not in self.config_dict:
            self.config_dict['ChanLabesl'] = [''] * NC

        # Name of the display module
        module_name = self.config_dict['DisplayModule']

        # TODO: Check if there are safer ways for doing this
        # import relevant library
        try:
            command = 'from .' + module_name + ' import *'
            exec(command, globals(), locals())
        except Exception as e:
            print(' !!! Display: failed to import module - exiting')
            print(str(e))
            sys.exit(1)

        try:
            command = 'global DG; DG = ' + module_name + '(self.config_dict)'
            exec(command, globals(), locals())
        except Exception as e:
            print(' !!! Display: failed to initialize module - exiting')
            print(str(e))
            sys.exit(1)

        # Init the imported display module
        DG.init()

        # Get the figure from the display module and add it to the widget of the window
        dynamic_canvas = FigureCanvas(DG.fig)
        layout.addWidget(dynamic_canvas)
        layout.addLayout(button_layout)

        button_start = QPushButton("Start")
        # button_start.setEnabled(False)
        button_start.clicked.connect(self.button_start_clicked)
        button_layout.addWidget(button_start)

        button_pause = QPushButton("Pause")
        button_layout.addWidget(button_pause)

        button_resume = QPushButton("Resume")
        button_layout.addWidget(button_resume)

        button_save_data = QPushButton("Save Data")
        button_layout.addWidget(button_save_data)

        button_save_graph = QPushButton("Save Graph")
        button_layout.addWidget(button_save_graph)

        button_end = QPushButton("End")
        button_end.clicked.connect(self.button_end_clicked)
        button_layout.addWidget(button_end)

        def button_end_clicked():
            self.cmd_queue.put('E')

        def cmd_pause():
            self.cmd_queue.put('P')

        def button_start_clicked():
            print("TODO!!!")

        def yield_event_from_queue():
            # receive data via a Queue from package multiprocessing
            cnt = 0
            lagging = False
            timestamp_last = time.time()

            while True:
                if not self.data_queue.empty():
                    data = self.data_queue.get()
                    if type(data) != np.ndarray:
                        break  # received end event
                    cnt += 1
                    yield cnt, data
                else:
                    yield None  # send empty event if no new data

                # check timing precision
                timestamp = time.time()
                delta_time = timestamp - timestamp_last
                if delta_time - interval < interval * 0.01:
                    if lagging:
                        lagging = False
                else:
                    if not lagging:
                        lagging = True
                # Update the timestamp
                timestamp_last = timestamp

            # end of yieldEvt_fromQ
            sys.exit()

        self.animation = anim.FuncAnimation(DG.fig, DG, yield_event_from_queue, interval=50, repeat=True, blit=True)

    def close_display(self):
        """
        Method to close the window
        :return: None
        """
        self.close()
