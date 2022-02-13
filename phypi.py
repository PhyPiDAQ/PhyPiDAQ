#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" run graphical user interface of PhyPiDAQ
"""

import sys, subprocess

if __name__ == "__main__":  # - - - - - - - - - - - - - - - - - - - -
    arg = '' if len(sys.argv)<2 else sys.argv[1]
    subprocess.call(['python3 -m phypidaq.runPhyPiUi ' + arg], shell=True)
