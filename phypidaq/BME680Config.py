import board
from adafruit_bme680 import Adafruit_BME680_I2C


class BME680Config(object):
    def __init__(self, config_dict=None):
        if config_dict is None:
            config_dict = {}
        if 'I2CADDR' in config_dict:
            self.I2CADDR = config_dict['I2CADDR']
        if 'NChannels' in config_dict:
            self.NChannels = config_dict["NChannels"]
            if self.NChannels < 1:
                self.NChannels = 1
        else:
            self.NChannels = 2
        if 'SeaLevelPressure' in config_dict:
            self.SeaLevelPressure = config_dict['SeaLevelPressure']

            if self.SeaLevelPressure < 0:
                self.SeaLevelPressure = 1013.25
                print("BMP280: sea level pressure set to %.3fA " % self.SeaLevelPressure)

        self.ChanLims = [[-40.0, 85.0], [300.0, 1100.0], [0.0, 1000.0], [0.0, 100.0], [0, 100000]]
        self.ChanNams = ['T', 'P', 'h', 'H', "R_VOC"]
        self.ChanUnits = ['°C', 'hPa', 'm', '%', "Ohm"]

    def init(self):
        i2c_bus = board.I2C()

        if hasattr(self, "I2CADDR"):
            self.sensor = Adafruit_BME680_I2C(i2c_bus, addr=self.I2CADDR)
        else:
            self.sensor = Adafruit_BME680_I2C(i2c_bus)

        if hasattr(self, "SeaLevelPressure"):
            self.sensor.sea_level_pressure = self.SeaLevelPressure

    def acquireData(self, buf):
        buf[0] = self.sensor.temperature
        if self.NChannels > 1:
            buf[1] = self.sensor.pressure
        if self.NChannels > 2:
            buf[2] = self.sensor.altitude
        if self.NChannels > 3:
            buf[3] = self.sensor.relative_humidity
        if self.NChannels > 4:
            buf[4] = self.sensor.gas

    def closeDevice(self):
        # Nothing to do here
        pass
