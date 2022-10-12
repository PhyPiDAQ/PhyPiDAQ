import time
from phypidaq.sensors.protocol import I2CSensor


class TSL45315Config:

    def __int__(self, config_dict=None):
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

        # Calculate NChannels and limits
        self.NChannels = len(self.channels)
        self.ChanNams = ["E_V"]
        self.ChanUnits = ["lx"]

        # Init the sensor
        self.i2c = I2CSensor(self.I2CADDR)

    def init(self):
        # Start normal operation mode
        self.i2c.write_register_byte(0x80, 0x03)

        # Set the integration time to 400ms
        self.i2c.write_register_byte(0x81, 0x00)

        # Sleep 0.2 seconds to apply the config to the sensor
        time.sleep(0.2)

    def acquireData(self, buf):
        data = self.i2c.read_register(0x84, 2)

        if "lux" in self.channels:
            buf[0] = data[1] * 256 + data[0]

    def closeDevice(self):
        # Nothing to do here
        pass
