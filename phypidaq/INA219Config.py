# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys

import board
from adafruit_ina219 import INA219, BusVoltageRange, ADCResolution, Gain

cname = "INA219Config"


class INA219Config(object):
    """current and voltage sensor INA219"""

    def __init__(self, confdict=None):
        # Define constants
        self.adcSwitch = {
            0: ADCResolution.ADCRES_9BIT_1S,
            1: ADCResolution.ADCRES_10BIT_1S,
            2: ADCResolution.ADCRES_11BIT_1S,
            3: ADCResolution.ADCRES_12BIT_1S,
            4: ADCResolution.ADCRES_12BIT_2S,
            5: ADCResolution.ADCRES_12BIT_4S,
            6: ADCResolution.ADCRES_12BIT_8S,
            7: ADCResolution.ADCRES_12BIT_16S,
            8: ADCResolution.ADCRES_12BIT_32S,
            9: ADCResolution.ADCRES_12BIT_64S,
           10: ADCResolution.ADCRES_12BIT_128S,
        }

        self.gainSwitch = {
            0: Gain.DIV_1_40MV,
            1: Gain.DIV_2_80MV,
            2: Gain.DIV_4_160MV,
            3: Gain.DIV_8_320MV,
        }

        if confdict == None:
            confdict = {}
        if 'I2CADDR' in confdict:
            self.I2CADDR = confdict['I2CADDR']
            print(cname + ": I2C address set to %x " % self.I2CADDR)
        if 'NChannels' in confdict:
            self.NChannels = confdict["NChannels"]
        else:
            self.NChannels = 2

        if 'maxAmp' in confdict:
            self.maxAmp = confdict['maxAmp']
        else:
            self.maxAmp = 3.19999
            print(cname + ": Current range set to %.3fA " % self.maxAmp)

        if 'maxVolt' in confdict:
            self.maxVolt = confdict['maxVolt']
        else:
            self.maxVolt = 32.

        if 'gainResolution' in confdict:
            self.gainResolution = confdict['gainResolution']
            self.autoGain = self.gainResolution == -1

            # Make sure, only valid gain resolutions are provided
            if self.gainResolution == -1:
                self.gainResolution = 0
        else:
            self.gainResolution = 0
            self.autoGain = False

        if 'busAdcResolution' in confdict:
            self.busAdcResolution = confdict['busAdcResolution']
        else:
            self.busAdcResolution = 0

        if 'shuntAdcResolution' in confdict:
            self.shuntAdcResolution = confdict['shuntAdcResolution']
        else:
            self.shuntAdcResolution = 0

        self.ChanLims = [[0., self.maxAmp],
                         [0., self.maxVolt],
                         [0., self.maxAmp * self.maxVolt]]
        self.ChanNams = ['I', 'U', 'P']
        self.ChanUnits = ['A', 'V', 'W']

    def init(self):

        if self.maxAmp > 3.2:
            print('!!! ' + cname + ": Current range must be < 3.2A")
            sys.exit(1)

        i2c_bus = board.I2C()
        if hasattr(self, "I2CADDR"):
            self.sensor = INA219(i2c_bus, addr=self.I2CADDR)
        else:
            self.sensor = INA219(i2c_bus)

        if self.maxVolt <= 16.:
            self.sensor.bus_voltage_range = BusVoltageRange.RANGE_16V
        elif self.maxVolt <= 32.:
            self.sensor.bus_voltage_range = BusVoltageRange.RANGE_32V
        else:
            print('!!! ' + cname + ": Voltage must be < 32.V")
            sys.exit(1)

        self.sensor.bus_adc_resolution = self.adcSwitch.get(self.busAdcResolution)
        self.sensor.shunt_adc_resolution = self.adcSwitch.get(self.shuntAdcResolution)

        self.sensor.gain = self.gainSwitch.get(self.gainResolution)

    def acquireData(self, buf):

        buf[0] = self.sensor.current / 1000.  # in Amps
        if self.NChannels > 1:
            buf[1] = self.sensor.bus_voltage
        if self.NChannels > 2:
            buf[2] = self.sensor.power

        if self.sensor.overflow:
            if self.autoGain and self.gainResolution != 3:
                # Try increasing the gain
                self.gainResolution += 1
                self.sensor.gain = self.gainSwitch.get(self.gainResolution)
            else:
                raise OverflowError('An internal overflow occurred!')

    def closeDevice(self):
        # Nothing to do here
        pass
