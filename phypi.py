#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run graphical user interface of PhyPiDAQ"""

import sys
import subprocess

if __name__ == "__main__":  # - - - - - - - - - - - - - - - - - - - -
    arg = '' if len(sys.argv) < 2 else sys.argv[1]
    subprocess.run(args=[sys.executable, "-m", "phypidaq.runPhyPiUi", arg])
