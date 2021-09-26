# -*- coding: utf-8 -*-

"""
Class providing graphical display and, optionally, a control interface
"""

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import numpy as np
import time
import sys
import multiprocessing as mp

import matplotlib
from PyQt5 import QtWidgets, QtGui, QtCore

matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QPushButton, QLabel, QFileDialog

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
        self.button_layout = QtWidgets.QHBoxLayout()

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

        # Define an empty animation
        self.animation = None

        # Set default options for graphical display
        if 'Interval' not in self.config_dict:
            self.config_dict['Interval'] = interval
        else:
            interval = self.config_dict['Interval']
        if interval < 0.05:
            print(" !!! read-out intervals < 0.05 s not reliable, setting to 0.05 s")
            self.config_dict['Interval'] = 0.05
            interval = 0.5
        self.interval = interval

        # XY mode is by default off
        if 'XYmode' not in self.config_dict:
            self.config_dict['XYmode'] = False

        # The default display is DataLogger
        if 'DisplayModule' not in self.config_dict:
            self.config_dict['DisplayModule'] = 'DataLogger'

        # Default mode is paused
        if 'startActive' not in self.config_dict:
            self.config_dict['startActive'] = False

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
        layout.addLayout(self.button_layout)

        self.figure = DG.fig

        self.button_start = QPushButton("Start")
        self.button_start.clicked.connect(self.cmd_start)

        self.button_pause = QPushButton("Pause")
        self.button_pause.clicked.connect(self.cmd_pause)

        self.button_resume = QPushButton("Resume")
        self.button_resume.clicked.connect(self.cmd_resume)

        self.button_save_data = QPushButton("Save Data")
        self.button_save_data.clicked.connect(self.cmd_save_data)

        self.button_save_graph = QPushButton("Save Graph")
        self.button_save_graph.clicked.connect(self.cmd_save_graph)

        self.button_end = QPushButton("End")
        self.button_end.clicked.connect(self.cmd_end)

        # Create a label for the passed time
        self.time_label = QLabel("0s")
        # Set the start time to a default value
        self.start_time = QtCore.QDateTime.currentSecsSinceEpoch()

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.display_time)

        print(self.config_dict)

        # Start automatically, if there are no controls
        if self.config_dict['DAQCntrl'] is False:
            self.button_layout.addWidget(self.time_label)
            self.cmd_start()
        else:
            # Add the buttons to the layout
            self.button_layout.addWidget(self.button_start)
            self.button_layout.addWidget(self.button_pause)
            self.button_layout.addWidget(self.button_resume)
            self.button_layout.addWidget(self.button_save_data)
            self.button_layout.addWidget(self.button_save_graph)
            self.button_layout.addWidget(self.button_end)
            self.button_layout.addWidget(self.time_label)

            if self.config_dict['startActive']:
                # Start the display
                self.cmd_start()
            else:
                # Disable all buttons except the start button
                self.button_pause.setEnabled(False)
                self.button_resume.setEnabled(False)
                self.button_save_data.setEnabled(False)
                self.button_save_graph.setEnabled(False)
                self.button_end.setEnabled(False)

    def cmd_start(self):
        # Disable the start button
        self.button_start.setEnabled(False)
        self.button_resume.setEnabled(False)

        # Enable all other buttons
        self.button_pause.setEnabled(True)
        self.button_save_data.setEnabled(True)
        self.button_save_graph.setEnabled(True)
        self.button_end.setEnabled(True)

        # Set the start time
        self.start_time = QtCore.QDateTime.currentSecsSinceEpoch()

        # Start the timer to display the time
        self.timer.start()

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
                if delta_time - self.interval < self.interval * 0.01:
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

    def cmd_end(self):
        self.cmd_queue.put('E')

    def cmd_pause(self):
        self.cmd_queue.put('P')
        self.button_pause.setEnabled(False)
        self.button_resume.setEnabled(True)

    def cmd_resume(self):
        self.cmd_queue.put('R')
        self.button_resume.setEnabled(False)
        self.button_pause.setEnabled(True)
        # Reset the start time
        self.start_time = QtCore.QDateTime.currentSecsSinceEpoch()

    def cmd_save_data(self):
        self.cmd_queue.put('s')
        # Pause the plotting
        self.cmd_pause()

    def cmd_save_graph(self):
        # Pause the plotting
        self.cmd_pause()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Graph", "plot.png", "PNG (*.png);;JPG (*.jpg *.jpeg)",
                                                   options=options)

        if file_name:
            if not (file_name.endswith(".png") or file_name.endswith(".jpg") or file_name.endswith(".jpeg")):
                # If the file extension doesn't match or isn't set, add it
                file_name = file_name + ".png"

            try:
                self.figure.savefig(file_name)
            except Exception as e:
                print(str(e))
                pass

        else:
            print("Aborting graph saving as no file was selected")

    def display_time(self):
        diff = QtCore.QDateTime.currentSecsSinceEpoch() - self.start_time
        self.time_label.setText(f"{diff}s")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Overriding the QMainWindow.closeEvent to handle the situations, when the users wants to close the window using
        the default window button.

        For further information on this method see:
        https://stackoverflow.com/questions/9249500/pyside-pyqt-detect-if-user-trying-to-close-window

        :param event: QtGui.QCloseEvent passed from the QApplication
        :return: None
        """
        self.cmd_end()
        event.accept()

    def close_display(self):
        """
        Method to close the window
        :return: None
        """
        self.close()
