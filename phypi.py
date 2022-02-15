#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" run graphical user interface of PhyPiDAQ
"""

import platform
import sys
import subprocess

if __name__ == "__main__":  # - - - - - - - - - - - - - - - - - - - -
    arg = '' if len(sys.argv) < 2 else sys.argv[1]
    if platform.system() == "Windows":
        subprocess.run(args=["python", "-m", "phypidaq.runPhyPiUi", arg])
    else:
        subprocess.run(args=["python3", "-m", "phypidaq.runPhyPiUi", arg])
