# -*- coding: utf-8 -*-

import board
import adafruit_adxl34x


class ADXL345Config(object):
    """digital accelerometer ADXL345 configuration and interface"""

    def __init__(self, config_dict=None):
        if config_dict is None:
            config_dict = {}

        # Set up properties
        self.NChannels = 3
        self.ChanNams = ['x', 'y', 'z']
        self.ChanUnits = ['m/s²', 'm/s²', 'm/s²']

        if 'I2CADDR' in config_dict:
            self.I2CADDR = config_dict['I2CADDR']

        if 'Range' in config_dict:
            if config_dict['Range'] in ["2G", "4G", "8G", "16G"]:
                self.range = config_dict['Range']
            else:
                # Passed parameter is not valid formatted
                self.range = "2G"
        else:
            # Nothing was specified therefore using default
            self.range = "2G"

        if self.range == '2G':
            self.range_config = adafruit_adxl34x.Range.RANGE_2_G
            r = 2
        elif self.range == '4G':
            self.range_config = adafruit_adxl34x.Range.RANGE_4_G
            r = 4
        elif self.range == '8G':
            self.range_config = adafruit_adxl34x.Range.RANGE_8_G
            r = 8
        elif self.range == '16G':
            self.range_config = adafruit_adxl34x.Range.RANGE_16_G
            r = 16
        else:
            raise ValueError("ADXL345 initialization error! Invalid value for range")

        self.ChanLims = [[-r * 10.0, r * 10.0], [-r * 10.0, r * 10.0], [-r * 10.0, r * 10.0]]

        # Internal hardware properties
        self.sensor = None

    def init(self):
        # Set up hardware
        i2c = board.I2C()

        # Set up sensor
        if hasattr(self, "I2CADDR"):
            self.sensor = adafruit_adxl34x.ADXL345(i2c, address=self.I2CADDR)
        else:
            self.sensor = adafruit_adxl34x.ADXL345(i2c)

    def acquireData(self, buf):
        buf[0], buf[1], buf[2] = self.sensor.acceleration

    def closeDevice(self):
        # Nothing to do here
        pass
