#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""read_18B20.py
this script illustrates the general usage of package phypidaq
prints data read from a digital sensor  (DS18B20 Temperature Sensor)
"""

import time
import numpy as np

# import module controlling readout device
from phypidaq.DS18B20Config import *

# create an instance of the device
device = DS18B20Config()

# initialize the device
device.init()

# reserve space for data (here only one channel)
dat = np.array([0.0])

print(" starting readout,     type <ctrl-C> to stop")

# read-out interval in s
dt = 2.0
# start time
T0 = time.time()

# readout loop, stop with <ctrl>-C
while True:
    device.acquireData(dat)
    dT = time.time() - T0
    print("%.2g, %.4g" % (dT, dat))
    time.sleep(dt)
