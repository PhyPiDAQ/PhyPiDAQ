#!/usr/bin/env python3

"""script soudcardOsci.py

read data from soundcard and disply wave forms

application example for class SoundCardOsci
"""

import time

from phypidaq.soundcardOsci import SoundCardOsci, scOsciDisplay


# set parameters
sampling_rate = 48000  # 44100, 48000, 96000 or 192000
sample_size = 2048
channels = 2  # 1 or 2
display_range = 2**12  # maximum is 2**15 for 16bit sound card
run_seconds = 60  # run-time in seconds

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
Display = scOsciDisplay(confdict=confd)

# start data acquisition loop
t_start = time.time()
t0 = t_start
n0 = 0
print("\n --> reading from Soundcard ...          <cntrlC to exit>")
try:
    runtime = 0.0
    t_lastupd = 0.0
    while runtime < run_seconds:
        count, data = scO()  # get data
        now = time.time()  # time stamp
        runtime = now - t_start
        Display(data)  # show data
        # update status display line
        if runtime - t_lastupd > 1:
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
