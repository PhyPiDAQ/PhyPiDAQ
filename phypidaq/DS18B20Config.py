# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys

# import relevant pieces for DS18B20
from w1thermsensor import W1ThermSensor, Unit


class DS18B20Config(object):
    """digital thermometer DS18B20Config configuration and interface"""

    def __init__(self, confdict=None):
        if confdict is None:
            confdict = {}

        # -- number of Channels
        self.NChannels = 1

        # -- unit configuration DS18B20
        if "Unit" in confdict:
            if confdict["Unit"] == "DEGREES_F":
                self.unit = Unit.DEGREES_F
                self.ChanLims = [[14.0, 230.0]]
            elif confdict["Unit"] == "KELVIN":
                self.unit = Unit.KELVIN
                self.ChanLims = [[263.15, 383.15]]
            else:
                self.unit = Unit.DEGREES_C
                self.ChanLims = [[-10.0, 110.0]]
        else:
            self.unit = Unit.DEGREES_C
            self.ChanLims = [[-10.0, 110.0]]

        self.DS18B20 = None

        # provide configuration parameters
        self.ChanNams = ['DS18B20']

    def init(self):
        # Hardware configuration:
        try:
            # Create an DS18B20 instance.
            self.DS18B20 = W1ThermSensor()
        except Exception as e:
            print("DS18B20Config: Error initialising device - exit")
            print(str(e))
            sys.exit(1)

    def acquireData(self, buf):
        buf[0] = self.DS18B20.get_temperature(self.unit)

    def closeDevice(self):
        # nothing to do here
        pass
