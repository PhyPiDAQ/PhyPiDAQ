#!/usr/bin/python3
"""set_MCP4725
   set voltage on DAC MCP4725
"""
from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys
# Import the MCP4725 module and other required adafruit modules
import board
import busio
import adafruit_mcp4725

# Initialize I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create a DAC instance.
dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)

V = 0.  # default 0V
if len(sys.argv) > 1:
    V = float(sys.argv[1])

VB = 5.

# Check if the passed value is in range
if V > VB:
    V = VB
if V < 0:
    V = 0

print('Setting voltage=%.2f' % V)
try:
    dac.normalized_value = V/VB

except KeyboardInterrupt:
    print("Error setting voltage")

finally:
    sys.exit(0)
