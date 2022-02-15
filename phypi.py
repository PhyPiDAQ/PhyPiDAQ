#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" run graphical user interface of PhyPiDAQ
"""

import sys, subprocess

if __name__ == "__main__":  # - - - - - - - - - - - - - - - - - - - -
    # get commandline arguments 
    arg = '' if len(sys.argv)<2 else sys.argv[1]    
    # sys.executable is the present python interpreter,
    #  restart it and run GUI of PhyPiDAQ 
    subprocess.run(
        [sys.executable + ' -m phypidaq.runPhyPiUi ' + arg],
                   shell=True)
