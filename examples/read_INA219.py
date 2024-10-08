#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
read data from digital sensor:
this script illustrates the general usage of package phypidaq prints data read from a digital sensor
INA219 Current & Voltage sensor
"""

import time
import numpy as np

# import module controlling readout device
from phypidaq.INA219Config import *

# create an instance of the device
config_dict = {"maxAmp": 0.1, "maxVolt": 16.0}
device = INA219Config(config_dict)

# initialize the device
device.init()

# reserve space for data (two channels here)
dat = np.array([0.0, 0.0])

print(" starting readout,     type <ctrl-C> to stop")

# read-out interval in s
dt = 2.0
# start time
T0 = time.time()

# readout loop, stop with <crtl>-C
while True:
    device.acquireData(dat)
    dT = time.time() - T0
    print("%.2g, %.4gmA %.4gV" % (dT, dat[0], dat[1]))
    time.sleep(dt)
