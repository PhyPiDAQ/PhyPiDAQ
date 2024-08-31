# -*- coding: utf-8 -*-
import board
import digitalio
import adafruit_max31855


class MAX31855Config(object):
    """MAX31855 configuration and interface"""

    def __init__(self, confdict=None):
        if confdict is None:
            confdict = {}

        # Set number of Channels
        self.NChannels = 1

        # Set up unit configuration for MAX31855
        if "Unit" in confdict:
            if confdict["Unit"] == "DEGREES_F":
                self.unit = confdict["Unit"]
                self.ChanLims = [[14.0, 482.0]]
            elif confdict["Unit"] == "KELVIN":
                self.unit = confdict["Unit"]
                self.ChanLims = [[263.15, 523.15]]
            else:
                self.unit = "DEGREES_C"
                self.ChanLims = [[-10.0, 250.0]]
        else:
            # Default to Celsius
            self.unit = "DEGREES_C"
            self.ChanLims = [[-10.0, 250.0]]

        # provide configuration parameters
        self.ChanNams = ['MAX31855']

        # Set up hardware properties
        self.spi = None
        self.cs = None
        self.sensor = None

    def init(self):
        # Init SPI and digital board IO
        self.spi = board.SPI()
        self.cs = digitalio.DigitalInOut(board.D5)

        # Hardware configuration:
        self.sensor = adafruit_max31855.MAX31855(self.spi, self.cs)

        # Check if the configuration was successful
        if self.sensor is None:
            raise AttributeError("Couldn't initialize sensor!")

    def acquireData(self, buf):
        if self.unit == "KELVIN":
            # Temperature in Kelvin
            buf[0] = self.sensor.temperature + 273.15
        elif self.unit == "DEGREES_F":
            # Temperature in degrees Fahrenheit
            buf[0] = (self.sensor.temperature * 1.8) + 32
        else:
            # Temperature in degrees Celsius
            buf[0] = self.sensor.temperature

    def closeDevice(self):
        # Nothing to do here
        pass
