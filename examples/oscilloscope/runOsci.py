#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Data visualisation
this script reads data from PicoScope
and displays them in oscilloscope mode

Usage: ./runOsci.py <Oscilloscope_config>.yaml
"""

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import sys
import time
import yaml
import numpy as np
import threading
import multiprocessing as mp

# import relevant pieces from picodaqa
import picodaqa.picoConfig
from picodaqa.mpOsci import mpOsci


# helper functions


def keyboard_input(cmd_queue):
    """read keyboard input, run as background-thread to avoid blocking"""

    while ACTIVE:
        kbdtxt = input(20 * " " + "type -> P(ause), R(esume), or (E)nd+ <ret> ")
        cmd_queue.put(kbdtxt)
        kbdtxt = ""


def stop_processes(process_list):
    """
    Close all running processes at end of run
    """
    for p in process_list:  # stop all sub-processes
        if p.is_alive():
            print("    terminating " + p.name)
            if p.is_alive():
                p.terminate()
            time.sleep(1.0)


if __name__ == "__main__":  # - - - - - - - - - - - - - - - - - - - - - -
    print("\n*==* script " + sys.argv[0] + " running \n")

    # check for / read command line arguments
    # read DAQ configuration file
    if len(sys.argv) >= 2:
        PSconfFile = sys.argv[1]
    else:
        PSconfFile = "PSOsci.yaml"
    print("    PS configuration from file " + PSconfFile)

    # read scope configuration file
    print("    Device configuration from file " + PSconfFile)
    try:
        with open(PSconfFile) as f:
            PSconfDict = yaml.load(f, Loader=yaml.Loader)
    except (OSError, yaml.YAMLError):
        print("     failed to read scope configuration file " + PSconfFile)
        exit(1)

    # configure and initialize PicoScope
    PSconf = picodaqa.picoConfig.PSconfig(PSconfDict)
    PSconf.init()
    # copy some of the important configuration variables
    NChannels = PSconf.NChannels  # number of channels in use
    TSampling = PSconf.TSampling  # sampling interval
    NSamples = PSconf.NSamples  # number of samples
    buf = np.zeros((NChannels, NSamples))  # data buffer for PicoScope driver

    thrds = []
    procs = []
    deltaT = 10.0  # max. update interval in ms
    cmdQ = mp.Queue(1)  # Queue for command input
    datQ = mp.Queue(1)  # Queue for data transfer to sub-process
    XY = True  # display Channel A vs. B if True
    name = "Oscilloscope"
    procs.append(mp.Process(name=name, target=mpOsci, args=(datQ, PSconf.OscConfDict, deltaT, name)))
    #                    Queue      config        interval name

    thrds.append(threading.Thread(name="kbdInput", target=keyboard_input, args=(cmdQ,)))
    #                           Queue

    # start subprocess(es)
    for prc in procs:
        prc.deamon = True
        prc.start()
        print(" -> starting process ", prc.name, " PID=", prc.pid)

    ACTIVE = True  # thread(s) active
    # start threads
    for thread in thrds:
        print(" -> starting thread ", thread.name)
        thread.deamon = True
        thread.start()

    DAQ_ACTIVE = True  # Data Acquisition active
    # -- LOOP
    sig = np.zeros(NChannels)
    try:
        cnt = 0
        T0 = time.time()
        while True:
            if DAQ_ACTIVE:
                cnt += 1
                PSconf.acquireData(buf)  # read data from PicoScope
                # construct an "event" like BufferMan.py does and send via Queue
                datQ.put((cnt, time.time() - T0, buf))

            # check for keyboard input
            if not cmdQ.empty():
                cmd = cmdQ.get()
                if cmd == "E":
                    print("\n" + sys.argv[0] + ": End command received - closing down")
                    ACTIVE = False
                    break
                elif cmd == "P":
                    DAQ_ACTIVE = False
                elif cmd == "R":
                    DAQ_ACTIVE = True

    except KeyboardInterrupt:
        DAQ_ACTIVE = False
        ACTIVE = False
        print("\n" + sys.argv[0] + ": keyboard interrupt - closing down ...")

    finally:
        PSconf.closeDevice()  # close down hardware device
        time.sleep(1.0)
        stop_processes(procs)  # stop all sub-processes in list
        print("*==* " + sys.argv[0] + ": normal end")
