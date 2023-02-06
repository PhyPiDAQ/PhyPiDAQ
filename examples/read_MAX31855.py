#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np

# import module controlling readout device
from phypidaq.MAX31855Config import *

# create an instance of the device
device = MAX31855Config()

# Initialize the device
device.init()

# reserve space for data (four channels here)
data = np.array([0., 0., 0., 0.])

print('Starting readout. Type <Ctrl-C> to stop')

# read-out interval in s
dt = 1.
# start time
T0 = time.time()

# Readout loop, stop with <Ctrl>-C
while True:
    device.acquireData(data)
    dT = time.time() - T0
    print('%.2g, %.4g°C' % (dT, data[0]))
    time.sleep(dt)
