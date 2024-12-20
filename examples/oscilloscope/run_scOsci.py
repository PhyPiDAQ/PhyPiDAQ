#!/usr/bin/env python3

"""script run_scOsci.py

read data from soundcard and disply wave forms

application example for class SoundCardOsci

adjust the parameters in the header part of the script to meet the
needs of you specific use case:

  - sampling rate of the sound card
  - the sample size
  - number of channels
  - the display range
  - trgActive #  True to activate Trigger
  - trgLevel  # trigger level in ADC counts
  - trgFalling  # trigger mode falling edge if True
"""

import time
from phypidaq.soundcardOsci import SoundCardOsci, scOsciDisplay

# set parameters
sampling_rate = 96000  # 44100, 48000, 96000 or 192000
sample_size = 1024
channels = 1  # 1 or 2
display_range = 2**13  # maximum is 2**15 for 16bit sound card
trgActive = True  # activate (software) trigger
trgLevel = 2000   # trigger level
trgFalling = False  # mode falling, False means rising
trgChan= 1          # trigger channel
run_seconds = 60  # run-time in seconds
upd_interval = 1.0  # update interval for status line

# create a configuration dictionary
confd = {
    "sampling_rate": sampling_rate,
    "number_of_samples": sample_size,
    "channels": [i + 1 for i in range(channels)],
    "range": display_range,
    "trgActive": trgActive,
    "trgChan": trgChan,
    "trgThreshold": trgLevel,
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
