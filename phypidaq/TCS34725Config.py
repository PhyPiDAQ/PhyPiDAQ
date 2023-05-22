# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

# import relevant pieces for TCS34725 RGB (color) sensor
import board
import adafruit_tcs34725


class TCS34725Config(object):
    """ TC34725 configuration and interface"""

    def __init__(self, confdict=None):
        if confdict is None:
            confdict = {}

        # -- number of Channels
        if 'NChannels' in confdict:
            self.NChannels = confdict['NChannels']
        else:
            self.NChannels = 3

        if 'Gain' in confdict:
            gains = (1, 4, 16, 60)
            if isinstance(confdict["Gain"], int):
                self.gain = gains(confdict['Gain'])
            else:
                self.gain = 4
        else:
            self.gain = 4
            # Possible gain values:
            #  - TCS34725_GAIN_1X
            #  - TCS34725_GAIN_4X  (default)
            #  - TCS34725_GAIN_16X
            #  - TCS34725_GAIN_60X

        if 'IntegrationTime' in confdict:
            Int_Times = (2.4, 24, 50, 101, 154, 700)
            self.IntTime = Int_Times(confdict['IntegrationTime'])
        else:
            self.IntT = 2.4

        if 'I2CADDR' in confdict:
            self.I2CAddr = confdict['I2CADDR']
            print("TCS34725: I2C address set to %x " % self.I2CAddr)
        else:
            self.I2CAddr = 0x29  # use default

        if 'busnum' in confdict:
            self.busnum = confdict['busnum']
            print("TCS34725: bus number set to %x " % self.busnum)
        else:
            self.busnum = 1  # use default

        # provide configuration parameters
        self.ChanNams = ['R', 'G', 'B', 'c']
        self.ChanLims = [[0., 1.]] * self.NChannels
        self.sensor = None

    def init(self):
        # Hardware configuration:

        # Create sensor object, communicating over the board's default I2C bus
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.sensor = adafruit_tcs34725.TCS34725(i2c, address=self.I2CAddr)

        # Change sensor integration time to values between 2.4 and 614.4 milliseconds
        self.sensor.integration_time = self.IntTime

        # Change sensor gain to 1, 4, 16, or 60
        self.sensor.gain = self.gain

    def acquireData(self, buf):

        # Read the R, G, B, C color data.
        if self.NChannels == 1:
            buf[0] = self.sensor.lux
        else:
            colors = self.sensor.color_rgb_bytes
            buf[0] = colors[0]
            buf[1] = colors[1]
            buf[2] = colors[2]
            if self.NChannels > 3:
                buf[3] = self.sensor.lux

    def closeDevice(self):
        # nothing to do here
        pass
