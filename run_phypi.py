#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" script run_phypi.py to execute PhyPiDAQ

    usage: run_phypi.py <config>.daq
"""

from phypidaq.runPhyPiDAQ import *
from phypidaq.helpers import keyboard_wait
import sys

if __name__ == "__main__":  # - - - - - - - - - - - - - - - - - - - -

    if len(sys.argv) != 2:
        print("\n!!! run_phypi.py usage:\n" + 10 * ' ' + "run_phypi.py <config>.daq\n")
        prompt = "    starting demo mode from configuration PhyPiDemo.daq" \
                 + "\n" + 25 * ' ' + "type <ret> to continue, 'E+<ret>' to exit -> "
        answer = keyboard_wait(prompt)
        if answer == '':
            sys.argv.append("PhyPiDemo.daq")
        else:
            print("     exiting")
            sys.exit(1)

    daq = runPhyPiDAQ(verbose=1)
    # 0: only errors are printed
    # 1: normal output
    # 2: verbose output

    daq.setup()
    print("DAQ set-up:\n", yaml.dump(daq.PhyPiConfDict))

    daq.run()
