#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import numpy as np

# Import module controlling readout device
from phypidaq.BME680Config import *

# Create a config dictionary, to print all four channels
config_dict = {'NChannels': 5}

# Create an instance of the device
device = BME680Config(config_dict=config_dict)

# Initialize the device
device.init()

# Reserve space for data (five channels here)
data = np.array([0., 0., 0., 0., 0.])

# Print message
print("Starting burn-in-process for MOX to adjust.")
print("Duration: 48h")

start_time = int(time.time())
duration = 2 * 1440
print(start_time)

# Loop to make the reading
for i in range(duration):
    # Read data
    device.acquireData(data)
    # Print progress
    bar_len = 60
    filled_len = int(round(bar_len * i / float(duration)))

    percents = round(100.0 * i / float(duration), 1)
    bar = '#' * filled_len + ' ' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%%\r' % (bar, percents))
    sys.stdout.flush()
    # Sleep a minute
    time.sleep(60)

print("Finished!")
