#!/usr/bin/env python3

"""script scGammaDetektor.py

read data from soundcard and
 - display oscillogram of raw wave forms
 - disply individual events as flash and show wave form data (if available)
 - store time stamps in file

This is an application example for the class phypidaq.SoundCardOsci.
"""

import sys
import argparse
import time
import numpy as np
import threading
import multiprocessing as mp
from phypidaq.soundcardOsci import SoundCardOsci, scOsciDisplay
from phypidaq.helpers import DAQwait
from phypidaq.DisplayPoissonEvent import DisplayPoissonEvent


def keyboard_input(cmd_queue):
    """Read keyboard input and send to Qeueu, runing as background-thread to avoid blocking"""

    while active:
        cmd = input()
        cmd_queue.put(cmd)
        if cmd == "E":
            break


def showFlash(mpQ, interval):
    """Background process to show Poisson event as a flashing circle

    relies on class DisplayPoissionEvent
    """
    flasher = DisplayPoissonEvent(mpQ, interval=interval)
    flasher()


def runDAQ():
    """run data acquistion as thread"""
    t_start = time.time()
    t_lastupd = t_start
    osc_wait_time = 0.1
    maxADC = np.float32(display_range)
    while active:
        try:
            # get data
            _d = scO()
            if _d is None:  #
                return
            count, trg_idx, data = _d
            now = time.time()
            # save to file
            if csvfile is not None:
                print(f"{count}, {now-t_start}", file=csvfile)
                if count % 5:
                    csvfile.flush()
            # show oscillogram of raw wave form
            if oscDisplay is not None:
                if (now - t_lastupd) > osc_wait_time:
                    oscDisplay(data, trg_idx)  # show subset of data
                    t_lastupd = now
            # show events
            if showevents:
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
        except Exception:
            return


# parse command line arguments
parser = argparse.ArgumentParser(
    description="Read waveforms from soundcard and display and optionally store data"
)
parser.add_argument(
    "-q", "--quiet", action="store_true", help="no status output to terminal"
)
parser.add_argument(
    "-o", "--oscilloscope", action="store_true", help="oscilloscope display"
)
parser.add_argument(
    "-n", "--noeventdisplay", action="store_true", help="deactivate event display"
)
parser.add_argument(
    "-f", "--file", type=str, default="", help="base filename to store results"
)
parser.add_argument("-t", "--time", type=int, default=3600, help="run time in seconds")
#
parser.add_argument(
    "-s",
    "--samplingrate",
    type=int,
    choices={44100, 48000, 96000, 192000},
    default=96000,
    help="sampling rate",
)
parser.add_argument(
    "-c", "--channels", type=int, choices={1, 2}, default=1, help="number of channels"
)
parser.add_argument(
    "-l", "--trglevel", type=float, default=5000, help="level of trigger"
)
parser.add_argument("--trgfalling", action="store_true", help="trigger falling edge")
parser.add_argument(
    "-d", "--trgdeactivate", action="store_true", help="deactivate triggering"
)
parser.add_argument(
    "-z", "--samplesize", type=int, default=256, help="number of samples per read"
)
parser.add_argument("-r", "--range", type=float, default=2**14, help="display range")
#
parser.add_argument(
    "-i", "--interval", type=float, default=30.0, help="time bin for rate display"
)
#
args = parser.parse_args()
# - parameters to control the scrpt
quiet = args.quiet
osc_display = args.oscilloscope
showevents = not args.noeventdisplay
filename = args.file
run_seconds = args.time
# - set-up of class phyipdaq.SoundCardOsci
sampling_rate = args.samplingrate
sample_size = args.samplesize
channels = args.channels
display_range = args.range  # maximum is 2**15 for 16bit sound card
trgThreshold = args.trglevel
trgFalling = args.trgfalling
trgActive = not args.trgdeactivate
# - parameter for DisplayPoissonEvent
interval = args.interval

# create a configuration dictionary for SoundCardOsci
confd = {
    "sampling_rate": sampling_rate,
    "number_of_samples": sample_size,
    "channels": [i + 1 for i in range(channels)],
    "range": display_range,
    "trgActive": trgActive,
    "trgThreshold": trgThreshold,
    "trgFalling": trgFalling,
}

csvfile = None
if filename != "":
    timestamp = time.strftime("%y%m%d-%H%M", time.localtime())
    fn = filename + "_" + timestamp + ".csv"
    csvfile = open(fn, "w")
    csvfile.write("event_numer, event_time[s]\n")


# background process to show event in real-time as "flash"
flasherQ = mp.Queue()
flasherProc = mp.Process(
    name="Gamma Event",
    target=showFlash,
    args=(flasherQ, interval),
)
flasherProc.start()

# initialze sound card interface
scO = SoundCardOsci(confdict=confd)
scO.init()
# process to read oscilloscope and display wave forms
if osc_display:
    oscDisplay = scOsciDisplay(confdict=confd)
else:
    oscDisplay = None
osciThread = threading.Thread(target=runDAQ, args=(), daemon=True)


# set up keyboard control
active = True
cmdQ = mp.Queue()  # Queue for command input from keyboard
kbdthread = threading.Thread(
    name="kbdInput", target=keyboard_input, args=(cmdQ,)
).start()

# start data acquisition loop
wait_time = 1.0
wait = DAQwait(wait_time)
n0 = 0
t_start = time.time()
t0 = t_start
runtime = 0.0
print("\n --> start reading from Soundcard ... ")
osciThread.start()
if not flasherProc.is_alive():
    print("!!! failed to start event display")
try:
    # daq loop
    while runtime < run_seconds:
        if not cmdQ.empty():
            cmd = cmdQ.get()
            if cmd == "E":
                break  # end cleanly
        wait()
        # calculate trigger rate and update status display line
        count = scO.event_count
        now = time.time()  # time stamp
        runtime = now - t_start
        rate = (count - n0) / (now - t0)
        n0 = count
        t0 = now
        print(
            f"active: {runtime:.1f}  triggers: {count}  rate: {rate:.1f} Hz     -> type 'E' to end",
            10 * " ",
            end="\r",
        )
    # -- end while
    print("\n               ... stop reading data")
except KeyboardInterrupt:
    print("\n" + " !!! keyboard interrupt - ending ...")
finally:
    input(30 * " " + "Finished !  Type <ret> to exit -> ")
    print("             closing Soundcard stream")
    active = False
    if csvfile is not None:
        csvfile.close()
    flasherProc.terminate()
    time.sleep(0.3)
    scO.close()
    sys.exit(0)
