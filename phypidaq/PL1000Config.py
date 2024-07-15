import numpy as np
import sys

# import relevant pieces from picodaqa ...
from picodaqa.picolog1000Config import picolog1000config


class PL1000Config(object):
    """configuratin and interface for PicoLog 1000 Series data loggers"""

    def __init__(self, confdict=None):
        if confdict is None:
            self.confdict = {}
            print('No configuration specified - using channel 1')
        else:
            self.confdict = confdict

    def init(self):
        # initialize PicoScope and retrieve config parameters
        self.PL = picolog1000config(self.confdict)
        self.PL.init()

        # collect/set configuration parameters
        self.NChannels = self.PL.NChannels
        self.ChanNams = ["ch"+str(self.PL.channels[i]) for i in range(self.NChannels)]
        self.ChanLims = [[0., 2500.]] * self.NChannels
        self.ChanUnits = ['mV'] * self.NChannels


    def acquireData(self, buf):
        # read data from PicoLog

        data = self.PL()  # read data from PicoLog
        for i in range(self.NChannels):
            buf[i] = data[i]

    def closeDevice(self):
        self.PL.close()
