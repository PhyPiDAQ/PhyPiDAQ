#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""script read_Pipe.py
usage: read_Pipe [name of pipe]

Read data from a named linux pipe
filled by run_phypi.py with option
DAQfifo: <name of pipe>
"""

import sys
import os
import errno

if len(sys.argv) >= 2:
    FiFo = sys.argv[1]
else:
    FiFo = "PhyPiDAQ.fifo"
print("*==* ", sys.argv[0], " Lese Daten aus Pipe", FiFo)

# create a fifo, ignore error if it already exists
try:
    os.mkfifo(FiFo)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# with os.open(FiFo, os.O_RDONLY | os.O_NONBLOCK) as f:
with open(FiFo) as f:
    # inp = f.read()  f.readline()
    for inp in f:
        if inp == "\n":
            break
        print("Read: %s " % inp, end="")
print("        empty line received, ending")
