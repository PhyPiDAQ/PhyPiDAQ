import board

from adafruit_bmp3xx import BMP3XX_I2C


class BMP388Config(object):

    def __init__(self, config_dict=None):

        if config_dict is None:
            config_dict = {}
        if 'I2CADDR' in config_dict:
            self.I2CADDR = config_dict['I2CADDR']
        if 'NChannels' in config_dict:
            self.NChannels = config_dict["NChannels"]
            if self.NChannels < 1:
                self.NChannels = 1
            elif self.NChannels > 3:
                self.NChannels = 3
        else:
            self.NChannels = 2
        if 'SeaLevelPressure' in config_dict:
            self.SeaLevelPressure = config_dict['SeaLevelPressure']

            if self.SeaLevelPressure < 0:
                self.SeaLevelPressure = 1013.25
                print("BMP388: sea level pressure set to %.3fA " % self.SeaLevelPressure)

        if self.NChannels == 1:
            self.ChanLims = [[-40., 85.]]
            self.ChanNams = ['T']
            self.ChanUnits = ['°C']
        elif self.NChannels == 2:
            self.ChanLims = [[-40., 85.], [300., 1100.]]
            self.ChanNams = ['T', 'P']
            self.ChanUnits = ['°C', 'hPa']
        elif self.NChannels == 3:
            self.ChanLims = [[-40., 85.], [300., 1100.], [0., 1000.]]
            self.ChanNams = ['T', 'P', 'h']
            self.ChanUnits = ['°C', 'hPa', 'm']

        self.sensor = None

    def init(self):
        i2c_bus = board.I2C()

        if hasattr(self, "I2CADDR"):
            self.sensor = BMP3XX_I2C(i2c_bus, addr=self.I2CADDR)
        else:
            self.sensor = BMP3XX_I2C(i2c_bus)

        if hasattr(self, "SeaLevelPressure"):
            self.sensor.sea_level_pressure = self.SeaLevelPressure

    def acquireData(self, buf):
        buf[0] = self.sensor.temperature
        if self.NChannels > 1:
            buf[1] = self.sensor.pressure
        if self.NChannels > 2:
            buf[2] = self.sensor.altitude

    def closeDevice(self):
        # Nothing to do here
        pass
