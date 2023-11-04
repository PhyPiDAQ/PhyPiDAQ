#!/usr/bin/python3
"""PoissonFlash:  

    Generate a sequence of random events with constant expectation value 
    for the event rate; display as flashing circle and show observed
    event rate in time intervals corresponding to a given Poisson mean. 

    Type *./poissonFlash.py --help* to see the list of options. 

    Description:

    A background process, PoissonEventGenerator(), generates events
    (via a timed sleep) and puts the time stamp (time since start)
    in a multi-processing queue. This time stamp is read and stored 
    by the main process and also injected into the input queue of the 
    background process showFlash(), which displays a short flash of
    a circular object. This graphical representation can be seen as a 
    flash of light in a detector. The display also shows the number of
    observed events in fixed time intervals as a history plot. 

    By replacemnt of the software generator by a readout-process of
    a real detector this simple script can also serve as an event
    display and simple analyzer of a real Poisson process.  

"""

import argparse
import multiprocessing as mp
import sys
import time

import numpy as np
import random

from phypidaq.DisplayPoissonEvent import *


# ---- helper functions -------


def showFlash(mpQ, rate, mean):
    """Background process to show Poisson event as a flashing circle

    relies on class DisplayPoissionEvent
    """
    flasher = DisplayPoissonEvent(mpQ, rate, mean)
    flasher()


def poissonEventGenerator(mpQ, rate):
    """Generate sequence of signals corresponding to a Poisson process"""
    tau = 1.0 / rate
    dtcum = 0.0
    T0 = time.time()
    while True:
        # show flash
        t = time.time() - T0
        mpQ.put(t)  # send event time
        # exponentially distributed wait time
        dt_wait = -tau * np.log(random.uniform(0.0, 1.0))
        # correct for time lags
        dt_cor = max(0.9 * dt_wait, dt_wait + dtcum - t)
        dtcum += dt_wait
        # wait ...
        if dt_cor > 0.002:
            time.sleep(dt_cor)
        print("  lag: %.1f ms " % ((dt_wait - dt_cor) * 1000), end='\r')


# ---- end helper functions

if __name__ == "__main__":  # ------------------------------------------------
    if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
        mp.freeze_support()

    # set data source
    eventSource = poissonEventGenerator

    # get command line  parameters
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-r', '--rate', type=float, default=1.0, help='average event rate in Hz')
    parser.add_argument('-m', '--mean', type=float, default=4.0, help='average Poisson mean for history ')
    parser.add_argument('-t', '--time', type=int, default=1800, help='run time in seconds')
    parser.add_argument('-H', '--history', type=int, default=500, help='max. number of data points to store')
    parser.add_argument('-f', '--file', type=str, default='', help='file name to store results')
    args = parser.parse_args()

    rate = args.rate
    mean = args.mean
    run_time = args.time
    timestamp = time.strftime('%y%m%d-%H%M', time.localtime())
    filename = args.file + '_' + timestamp + '.csv' if args.file != '' else ''
    NHistory = args.history
    times = np.zeros(NHistory)
    tau = 1.0 / args.rate

    # set up background process for flash display
    procs = []
    generatorQ = mp.Queue()  # Queue to spy on data transfer inside class Display
    flasherQ = mp.Queue()  # Queue to spy on data transfer inside class Display
    procs.append(
        mp.Process(
            name="showFlash",
            target=showFlash,
            args=(
                flasherQ,
                rate,
                mean,
            ),
        )
    )
    # generator process, must be last in list !
    procs.append(
        mp.Process(
            name="eventSource",
            target=eventSource,
            args=(
                generatorQ,
                rate,
            ),
        )
    )

    # start
    print(10 * ' ' + "flashing randomly with rate of %.3fs" % rate + " for %d s" % run_time)
    print(20 * ' ' + "<ctrl C> to end ", end='\r')

    for p in procs:
        p.start()

    icount = 0
    start_time = time.time()
    t = 0
    try:
        while t < run_time:
            t = generatorQ.get()
            flasherQ.put(t)
            times[icount % NHistory] = t
            icount += 1
        procs[-1].terminate()  # terminate generator
        a = input(15 * ' ' + "!!! time over, type <ret> to end ==> ")

    except KeyboardInterrupt:
        print("\n keyboard interrupt - ending   ")

    finally:
        # end processes
        flasherQ.put(-1)
        for p in procs:
            if p.is_alive():
                p.terminate()
        # sort and store data
        event_times = times[:icount].tolist() if icount <= NHistory else np.concatenate((times[icount:], times[:icount])).tolist()
        if filename != '':
            with open(filename, 'w') as csvfile:
                csvfile.write('event_times[s]\n')
                for i in range(icount):
                    csvfile.write(str(times[i]) + '\n')
            print("*==* script " + sys.argv[0] + " ended,  data saved to file " + filename)
