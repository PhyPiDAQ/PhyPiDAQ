#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""read_ADS1115.py
this script illustrates the general usage of package phypidaq
prints data read from an analog channel
"""

import time
import numpy as np

# import module controlling readout device
from phypidaq.ADS1115Config import *

# create an instance of the device
device = ADS1115Config()

# initialize the device
device.init()

# reserve space for data (here only one channel)
dat = np.array([0.0])

print(" starting readout,     type <ctrl-C> to stop")

# read-out interval in s
dt = 1.0
# start time
T0 = time.time()

# readout loop, stop with <ctrl>-C
while True:
    device.acquireData(dat)
    dT = time.time() - T0
    print("%.2g, %.4g" % (dT, dat))
    time.sleep(dt)
