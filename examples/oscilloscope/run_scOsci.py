#!/usr/bin/env python3

"""script run_scOsci.py

read data from soundcard and disply wave forms

application example for class SoundCardOsci
"""

import time
from phypidaq.soundcardOsci import SoundCardOsci, scOsciDisplay
from phypidaq.helpers import DAQwait


# set parameters
sampling_rate = 48000  # 44100, 48000, 96000 or 192000
sample_size = 2048
channels = 1  # 1 or 2
display_range = 2**13  # maximum is 2**15 for 16bit sound card
run_seconds = 60  # run-time in seconds
upd_interval = 1.  # update interval for status line

# create a configuration dictionary
confd = {
    "sampling_rate": sampling_rate,
    "number_of_samples": sample_size,
    "channels": [i + 1 for i in range(channels)],
    "range": display_range,
    "trgActive": True,
    "trgThreshold": 250,
    "trgFalling": False,
}

# initialze sound card interface
scO = SoundCardOsci(confdict=confd)
scO.init()
scD = scOsciDisplay(confdict=confd)

# start data acquisition loop
t_start = time.time()
t0 = t_start
n0 = 0
print("\n --> reading from Soundcard ...          <cntrlC to exit>")
try:
    runtime = 0.0
    t_lastupd = 0.0
    while runtime < run_seconds:
        count, trg_idx, data = scO()  # get data
        now = time.time()  # time stamp
        runtime = now - t_start
        scD.updateDisplay(count, trg_idx, data)  # show data
        # update status display line
        if runtime - t_lastupd > upd_interval:
            rate = (count - n0) / (now - t0)
            n0 = count
            t0 = now
            t_lastupd = runtime
            print(
                f"active: {runtime:.1f}   triggers: {count}   rate: {rate:.1f} Hz        ",
                end="\r",
            )
    print("\n" + " *** time over - ending ...")
except KeyboardInterrupt:
    print("\n" + " !!! keyboard interrupt - ending ...")
finally:
    print("             closing Soundcard stream")
    scO.close()
