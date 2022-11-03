import smbus
from typing import Optional, List


class I2CSensor:
    """Implementation of a I2C-Sensor"""

    def __init__(self, device_address: int, bus_id: Optional[int] = None) -> None:
        """
        Constructor for an i2c sensor

        :param device_address: int, i2c address of the device
        :param bus_id: int, default is 1 (Raspberry Pi with 40 GPIO pins)
        """

        # Set the device address
        self.device_address = device_address

        # Check, if a bus id was passed:
        if bus_id is None:
            # Default to bus id 1, if no bus id is passed.
            self.bus_id = 1
        # Handle the case, if a bus id is passed
        else:
            # Handle invalid input
            if bus_id < 0:
                # Throw an exception
                raise ValueError("Bus id can't be smaller than zero!")
            else:
                # Set the bus id, if the input was correct
                self.bus_id = bus_id

        # Initialize a bus object
        self.bus = smbus.SMBus(self.bus_id)

        # Check if the bus initialization was successful
        if self.bus is None:
            raise OSError("Couldn't create I2C bus object.")

    def read_register(self, register: int, length: Optional[int] = 1) -> List[bytes]:
        """
        Read from the device register.

        :param register: int
        :param length: optional int, default 1
        :return: list of bytes
        """

        # Check the length parameter
        if length < 1:
            raise ValueError("At least one byte needs to be read!")

        with self.bus as bus:
            block = bus.read_i2c_block_data(self.device_address, register, length)
            return block

    def write_register_byte(self, register: int, value: int) -> None:
        """
        Write to the device register.

        :param register: int
        :param value: int
        :return: none
        """
        with self.bus as bus:
            bus.write_byte_data(self.device_address, register, value)
