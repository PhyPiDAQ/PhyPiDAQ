import time
from .sensors.protocol import I2CSensor


class TSL45315Config:

    def __init__(self, config_dict=None):
        if config_dict is None:
            config_dict = {}
        if "I2CADDR" in config_dict:
            self.I2CADDR = config_dict["I2CADDR"]
        else:
            self.I2CADDR = 0x29

        if "Channels" in config_dict:
            if isinstance(config_dict["Channels"], list):
                self.channels = config_dict["Channels"]
                # Ensure, that all items are lowercase
                self.channels = [x.lower() for x in self.channels]
                # Filter list, to keep only valid channels
                self.channels = [x for x in self.channels if x in ["lux"]]
                # Check if enough channels are listed
                if len(self.channels) < 1:
                    # Set only one channel
                    print("No valid channels have been specified! Resetting it to following channels: lux")
                    self.channels = ["lux"]
            else:
                # Support only one channel
                self.channels = ["lux"]
        else:
            # Support only one channel
            self.channels = ["lux"]

        if "Multiplier" in config_dict:
            if isinstance(config_dict["Multiplier"], int):
                if config_dict["Multiplier"] == 1:
                    self.multiplier = 1
                elif config_dict["Multiplier"] == 2:
                    self.multiplier = 2
                elif config_dict["Multiplier"] == 4:
                    self.multiplier = 4
                else:
                    self.multiplier = 1
            else:
                self.multiplier = 1
        else:
            # Set default state
            self.multiplier = 1

        # Calculate NChannels and limits
        self.NChannels = len(self.channels)
        self.ChanNams = ["E_V"]
        self.ChanUnits = ["lx"]
        self.ChanLims = [[self.multiplier * 0, self.multiplier * 65535]]

        # Init the sensor
        self.i2c = I2CSensor(self.I2CADDR)

    def init(self):
        # Start normal operation mode
        self.i2c.write_register_byte(0x80, 0x03)

        if self.multiplier == 1:
            # Set the integration time to 400ms
            self.i2c.write_register_byte(0x81, 0x00)
        elif self.multiplier == 2:
            self.i2c.write_register_byte(0x81, 0x01)
        elif self.multiplier == 4:
            self.i2c.write_register_byte(0x81, 0x10)

        # Sleep 0.2 seconds to apply the config to the sensor
        time.sleep(0.2)

    def acquireData(self, buf):
        data = self.i2c.read_register(0x84, 2)

        if "lux" in self.channels:
            buf[0] = self.multiplier * (data[1] * 256 + data[0])

    def closeDevice(self):
        # Nothing to do here
        pass
