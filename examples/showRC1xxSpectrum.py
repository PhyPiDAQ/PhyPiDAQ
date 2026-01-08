#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""show_RC1xxSpectrum.py

Command-line example to read and display data from
RadiaCode Gamma Spectrometer with PhyPiDAQ
"""

import argparse
import sys
import time
import numpy as np
from phypidaq.RC1xxConfig import RC1xxConfig
from phypidaq.DisplayManager import DisplayManager

# parse command line arguments
parser = argparse.ArgumentParser(description="read and display spectrum from RadioCode Gamma Spectrometer")
parser.add_argument("--bluetooth-mac", type=str, required=False, help="bluetooth MAC address of radiascan device")
parser.add_argument(
    "-n", "--noreset", action="store_const", const=True, default=False, help="do not reset spectrum stored in device"
)
parser.add_argument("-i", "--interval", type=float, default=1.0, help="update interval")
parser.add_argument("-d", "--show_dose", action="store_const", const=True, default=False, help="only show dose")
args = parser.parse_args()

# process control in PhyPiDAQ relies on a dictionary; set it up first
confdict = {}

confdict["show_spectrum"] = not args.show_dose
confdict["bluetooth_mac"] = args.bluetooth_mac
confdict["reset"] = not args.noreset
confdict["Interval"] = args.interval

# initialize RadiaCode device
device = RC1xxConfig(confdict)
# this updats the dictionary with default parameters

# initialize data processing
device.init()

# complete confiuration dictionary from device information (if not supplied by user)
NChannels = device.NChannels
# complete configuration dictionary from defaults of driver
if "NChannels" not in confdict:
    confdict["NChannels"] = device.NChannels
if "ChanLimits" not in confdict:
    confdict["ChanLimits"] = device.ChanLims
if "ChanUnits" not in confdict:
    confdict["ChanUnits"] = device.ChanUnits
if "ChanNams" not in confdict:
    confdict["ChanNams"] = device.ChanNams

if "DisplayModule" not in confdict:
    if confdict["show_spectrum"]:
        confdict["DisplayModule"] = "DataSpectrum"
    else:
        confdict["DisplayModule"] = "DataLogger"

if "Interval" not in confdict:
    interval = 1.0
    confdict["Interval"] = interval
else:
    interval = confdict["Interval"]

# need additional information for Spectrum Display
if confdict["DisplayModule"] == "DataSpectrum":
    if "NBins" not in confdict:
        confdict["NBins"] = device.NBins
    if "Chan2Val" not in confdict:
        confdict["Chan2Val"] = device.Chan2E
    if "xName" not in confdict:
        confdict["xName"] = device.xName
    if "xUnit" not in confdict:
        confdict["xUnit"] = device.xUnit
elif confdict["DisplayModule"] == "DataLogger":
    if "NHistoryPoints" not in confdict:
        confdict["NHistoryPoints"] = 250

#  initialize Display
display = DisplayManager(config_dict=confdict)
display.init()

# reserve space for data
dat = np.zeros(device.NChannels)

T0 = time.time()
print(f"   {time.asctime(time.gmtime(T0))} script {sys.argv[0]} starting" + "         type <ctrl-C> to stop")
# readout loop, stop with <ctrl>-C
while True:
    device.acquireData(dat)
    dT = time.time() - T0
    if len(dat) <= 2:
        print(f"    active: {dT:.1f} s   counts: {dat[0]:.0f}   dose: {dat[1]:.3f}", end="          \r")
    display.showData(dat[:NChannels])
    time.sleep(interval)
