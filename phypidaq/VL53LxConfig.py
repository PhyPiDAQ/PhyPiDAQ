# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

# import relevant pieces for VL53L0X /1X distance sensor
import board
import adafruit_vl53l1x
import adafruit_vl53l0x

VL53L1_Max_Range = 4000.0
VL53L0_Max_Range = 1200.0


class VL53LxConfig(object):
    """VL53L1X and VL53L0X configuration and interface"""

    def __init__(self, confdict=None):
        if confdict is None:
            confdict = {}

        # Set the number of channels
        self.NChannels = 1  # sensor only has one channel

        # sensor type
        if 'type' in confdict:
            self.type = confdict['type']
            print("VL53Lx: sensor set to VL53L%iX " % self.type)
            # possible vales: 0, 1
        else:
            self.type = 1  # VL53LX1 is default

        if 'range' in confdict:
            if self.type == 1:
                # Check if the range has a valid value
                if confdict['range'] in [1, 2]:
                    # Set to the given value
                    self.range = confdict['range']
                else:
                    # Set to default
                    self.range = 1
            else:
                print("Skipping range for the VL53L0X")
        else:
            if self.type == 1:
                # Set the default if nothing is specified
                self.range = 1

        if 'I2CADDR' in confdict:
            self.I2CAddr = confdict['I2CADDR']
            print("VL53L1X: I2C address set to %x " % self.I2CAddr)
        else:
            self.I2CAddr = 0x29  # use default

        if 'busnum' in confdict:
            self.busnum = confdict['busnum']
            print("VL53L1X: bus number set to %x " % self.busnum)
        else:
            self.busnum = 1  # use default

        # provide channel parameters
        self.ChanNams = ['d']
        if self.type == 1:
            self.ChanLims = [[0.0, VL53L1_Max_Range]]
        else:
            self.ChanLims = [[0.0, VL53L0_Max_Range]]

        self.i2c = None
        self.sensor = None

    def init(self):
        # Hardware configuration:
        self.i2c = board.I2C()
        if self.type == 1:
            self.sensor = adafruit_vl53l1x.VL53L1X(self.i2c, address=self.I2CAddr)
            # Set the distance mode
            self.sensor.distance_mode = self.range
            # Start measuring
            self.sensor.start_ranging()
        else:
            self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c, address=self.I2CAddr)
            # Active the continuous mode
            self.sensor = self.sensor.continuous_mode()

    def acquireData(self, buf):
        if self.type == 1:
            if self.sensor.data_ready:
                buf[0] = self.sensor.distance * 10  # Return the distance in mm
        else:
            buf[0] = self.sensor.range  # distance in mm

    def closeDevice(self):
        if self.type == 1:
            # Stop measurements
            self.sensor.stop_ranging()
