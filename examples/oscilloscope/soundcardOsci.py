#!/usr/bin/env python3

"""script soudcardOsci.py

read data from soundcard and disply wave forms

application example for class SoundCardOsci
"""

import time
import threading
from phypidaq.soundcardOsci import SoundCardOsci, scOsciDisplay
from phypidaq.helpers import DAQwait


def displayOsci():
    t_lastupd = time.time()
    wait_time = 0.1
    while True:
        count, data = scO()  # get data
        if (time.time() - t_lastupd) > wait_time:
            Display(data)  # show subset of data
            t_lastupd = time.time()


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

osciThread = threading.Thread(target=displayOsci, args=(), daemon=True)

# start data acquisition loop
wait_time = 1.0
wait = DAQwait(wait_time)
n0 = 0
t_start = time.time()
t0 = t_start
runtime = 0.0
print("\n --> reading from Soundcard ...          <cntrlC to exit>")
try:
    osciThread.start()
    while runtime < run_seconds:
        wait()
        # calculate trigger rate and update status display line
        count = scO.event_count
        now = time.time()  # time stamp
        runtime = now - t_start
        rate = (count - n0) / (now - t0)
        n0 = count
        t0 = now
        print(
            f"active: {runtime:.1f}  triggers: {count}  rate: {rate:.1f} Hz",
            10 * " ",
            end="\r",
        )
    # -- end while
    print("\n" + " *** time over - ending ...")
except KeyboardInterrupt:
    print("\n" + " !!! keyboard interrupt - ending ...")
finally:
    print("             closing Soundcard stream")
    osciThread.terminate()
    scO.close()
