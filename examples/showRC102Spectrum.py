#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""show_RC102Spectrum.py
     this script reads the RadiaCode 102 Spectrometer
"""
import time, numpy as np
from phypidaq.RC10xConfig import RC10xConfig
from phypidaq.DisplayManager import DisplayManager

# set up a configuration dictionary
confdict = {}
### if 'show_spectrum' not in confdict:
#    confdict['show_spectrum'] = False
confdict['show_spectrum'] = True
confdict['reset']=True

# initialize RadiaCode device
device = RC10xConfig(confdict)
device.init()
NChannels = device.NChannels
# complete configuration dictionary from defaults of driver
if 'Chan2E' not in confdict:
    confdict['Chan2Val'] = device.Chan2E
if 'NChannels' not in confdict:
    confdict['NChannels'] = device.NChannels
if 'ChanLimits' not in confdict:
    confdict['ChanLimits'] = device.ChanLims
if 'ChanUnits' not in confdict:
    confdict['ChanUnits'] = device.ChanUnits
if 'ChanNams' not in confdict:
    confdict['ChanNams'] = device.ChanNams
    
if 'DisplayModule' not in confdict:
    if confdict['show_spectrum']:
       confdict['DisplayModule'] = 'DataSpectrum'
    else:
       confdict['DisplayModule'] = 'DataLogger'

if 'Interval' not in confdict:
    interval= 1. 
    confdict['Interval'] = interval 
# need additional information for Spectrum Display
if confdict['DisplayModule'] == 'DataSpectrum':
    confdict['NBins'] = device.NBins
    if 'xName' not in confdict:
        confdict['xName'] = device.xName
    if 'xUnit' not in confdict:
        confdict['xUnit'] = device.xUnit
       
#  initialize Display 
display = DisplayManager(config_dict=confdict)
display.init()

# reserve space for data (here only one channel)
dat = np.zeros(device.NChannels)

print(' starting readout,     type <ctrl-C> to stop')


# start time
T0 = time.time()


# readout loop, stop with <ctrl>-C
while True:
    device.acquireData(dat)
    dT = time.time() - T0
    if len(dat) <=2:
       print(f'    active: {dT:.1f} s   counts: {dat[0]:.0f}   dose: {dat[1]:.3f}', end='          \r')
    display.showData(dat[: NChannels])
    time.sleep(interval)
