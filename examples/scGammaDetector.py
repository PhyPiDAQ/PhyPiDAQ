#!/usr/bin/env python3

"""script scGammaDetektor.py

read data from soundcard and disply random events and wave form data

application example for class SoundCardOsci
"""

import time
import numpy as np
import threading
import multiprocessing as mp
from phypidaq.soundcardOsci import SoundCardOsci, scOsciDisplay
from phypidaq.helpers import DAQwait
from phypidaq.DisplayPoissonEvent import DisplayPoissonEvent


def showFlash(mpQ, interval):
    """Background process to show Poisson event as a flashing circle

    relies on class DisplayPoissionEvent
    """
    flasher = DisplayPoissonEvent(mpQ, interval=interval)
    flasher()


def runOsci():
    t_start = time.time()
    t_lastupd = t_start
    osc_wait_time = 0.1
    maxADC = np.float32(display_range)
    while active:
        try:
            _d = scO()  # get data
            if _d is None:  #
                return
            count, trg_idx, data = _d
            now = time.time()
            # extract data of size 100 around trigger
            if trg_idx is not None:
                i0 = max(trg_idx - 25, 0)
                i1 = min(trg_idx + 75, len(data[0]))
                d = i1 - i0
                if d < 100:
                    if i0 == 0:
                        i1 += 100 - d
                    else:
                        i0 -= 100 - d
                flasherQ.put((now - t_start, data[0][i0:i1] / maxADC))
            else:
                flasherQ.put(now - t_start)
            if Display is not None:
                if (now - t_lastupd) > osc_wait_time:
                    Display(data, trg_idx)  # show subset of data
                    t_lastupd = now
        except Exception:
            return


# set parameters
sampling_rate = 192000  # 44100, 48000, 96000 or 192000
sample_size = 250
channels = 1  # 1 or 2
display_range = 2**14  # maximum is 2**15 for 16bit sound card
run_seconds = 36000  # run-time in seconds
trgThreshold = 5500  # for CERN DIY particle detector
trgFalling = False
trgActive = True
interval = 60
osc_display = True

# create a configuration dictionary
confd = {
    "sampling_rate": sampling_rate,
    "number_of_samples": sample_size,
    "channels": [i + 1 for i in range(channels)],
    "range": display_range,
    "trgActive": trgActive,
    "trgThreshold": trgThreshold,
    "trgFalling": trgFalling,
}

# background process to show event in real-time as "flash"
flasherQ = mp.Queue()
flasherProc = mp.Process(
    name="Gamma Event",
    target=showFlash,
    args=(flasherQ, 60.0),
)
flasherProc.start()

# initialze sound card interface
scO = SoundCardOsci(confdict=confd)
scO.init()
# process to read oscilloscope and display wave forms
if osc_display:
    Display = scOsciDisplay(confdict=confd)
else:
    Display = None
osciThread = threading.Thread(target=runOsci, args=(), daemon=True)

# start data acquisition loop
wait_time = 1.0
wait = DAQwait(wait_time)
n0 = 0
t_start = time.time()
t0 = t_start
runtime = 0.0
print("\n --> reading from Soundcard ...          <cntrlC to exit>")
active = True
osciThread.start()
if not flasherProc.is_alive():
    print("!!! failed to start event display")
try:
    # daq loop
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
    active = False
    flasherProc.terminate()
    time.sleep(1.0)
    scO.close()
