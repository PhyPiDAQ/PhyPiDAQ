#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""display_analog.py
illustrates the general usage of package phypidaq
prints and displays data read from an analog channel
"""

import time
import numpy as np

# import module controlling readout device
from phypidaq.ADS1115Config import *

# import display
from phypidaq.DisplayManager import DisplayManager

# create an instance of device and display ...
device = ADS1115Config()
display = DisplayManager()
# ... and initialize
device.init()
display.init()

# reserve space for data (here only one channel)
dat = np.array([0.0])
interval = 1.0

print(" starting readout,     type <ctrl-C> to stop")
# start time
T0 = time.time()
try:
    # readout loop, stop with <ctrl>-C
    while True:
        device.acquireData(dat)
        dT = time.time() - T0
        print("%.1f, %.4g" % (dT, dat))
        display.showData(dat)
        time.sleep(interval)
except KeyboardInterrupt:
    print("ctrl-C received - ending")
    device.closeDevice()
    display.close()
