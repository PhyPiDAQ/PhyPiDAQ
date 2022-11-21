import board
import busio

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class ADS1115Config(object):
    """ADC ADS1115Config configuration and interface"""

    def __init__(self, config_dict=None):
        if config_dict is None:
            config_dict = {}

        # I2C address
        if "I2CADDR" in config_dict:
            self.I2CADDR = config_dict["I2CADDR"]
            print(f"ADS1115: I2C address set to {self.I2CADDR}")
        else:
            self.I2CADDR = 0x48  # use the default address of the sensor

        # Choose ADC-channels
        if "ADCChannels" in config_dict:
            self.ADCChannels = config_dict["ADCChannels"]
            # Filter list, to keep only valid channels and ensure that it's free of duplicates
            self.ADCChannels = list(set([x for x in self.ADCChannels if x in list(range(0, 4))]))
            # Check, that there is at least on channel
            if len(self.ADCChannels) == 0:
                print(f"ADS1115: No channels specified. Defaulting to channel 0")
                self.ADCChannels = [0]
        else:
            print("ADS1115: No channels specified. Defaulting to channel 0")
            self.ADCChannels = [0]
        # Calculate the number of channels
        self.NChannels = len(self.ADCChannels)

        # Select differential mode
        if 'DifModeChan' in config_dict:
            if len(config_dict['DifModeChan']) != len(self.ADCChannels):
                print("ADS1115: DifModeChan length doesn't match ADCChannels length. Disabling DifModeChan!")
                self.DifModeChan = [False for i, c in enumerate(self.ADCChannels)]
            else:
                self.DifModeChan = config_dict['DifModeChan']
        else:
            # Use normal mode by default
            self.DifModeChan = [False for i, c in enumerate(self.ADCChannels)]

        # Gain configuration for all channels
        if "Gain" in config_dict:
            if config_dict["Gain"] == '2/3':
                self.gain = 2 / 3
            elif config_dict["Gain"] in (1, 2, 4, 8, 16):
                self.gain = config_dict["Gain"]
            else:
                print("ADS1115: Invalid gain specified. Defaulting to 2/3!")
        else:
            # Default to default gain
            self.gain = 2 / 3

        # -- sample rate ADC ADS1115
        if "sampleRate" in config_dict:
            if config_dict["sampleRate"] in (8, 16, 32, 64, 128, 250, 475, 860):
                self.sampleRate = config_dict["sampleRate"]
            else:
                print("ADS1115: Invalid sample rate, defaulting to 860")
                self.sampleRate = 860
        else:
            # Set the default sample rate
            self.sampleRate = 860

        # Create the I2C bus
        self.i2c = None
        # Create a ADC interface
        self.adc = None

        # Create channel array
        self.channels = None

        self.ChanUnits = ['V'] * self.NChannels

        # Determine reference voltage for ADC calculation
        # possible values reference voltage
        self.ADCVRef = [6.114, 4.096, 2.048, 1.024, 0.512, 0.256]
        # determine the corresponding index
        self.VRef = [0., 0., 0., 0.]
        self.posGain = [2 / 3, 1, 2, 4, 8, 16]
        for i in range(self.NChannels):
            self.VRef[i] = self.ADCVRef[self.posGain.index(self.gain)]

        # provide configuration parameters
        self.ChanLims = [0., 0.] * self.NChannels
        self.ChanNams = [str(c) for c in self.ADCChannels]
        for i, c in enumerate(self.ADCChannels):
            if self.DifModeChan[i]:
                self.ChanLims[i] = [-self.VRef[i], self.VRef[i]]
                if c == 0:
                    self.ChanNams[i] = str(c) + '-1'
                else:
                    self.ChanNams[i] = str(c - 1) + '-3'
            else:
                self.ChanLims[i] = [0., self.VRef[i]]

    def init(self):
        # Hardware configuration:
        self.i2c = busio.I2C(board.SCL, board.SDA)

        self.adc = ADS.ADS1115(self.i2c, address=self.I2CADDR, gain=self.gain)

        # TODO: Finish channel logic

    def acquireData(self, buf):
        # TODO: Update function
        for i, c in enumerate(self.ADCChannels):
            # read data from ADC in differential mode
            if self.DifModeChan[i]:
                buf[i] = self.ADS.read_adc_difference(self.ADCChannels[i], gain=self.gain[i],
                                                      data_rate=self.sampleRate) * self.VRef[i] / 32767
            else:
                # read data from adc in single mode
                buf[i] = self.ADS.read_adc(self.ADCChannels[i], gain=self.gain[i],
                                           data_rate=self.sampleRate) * self.VRef[i] / 32767

    def closeDevice(self):
        # Nothing to do here
        pass
