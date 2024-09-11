#!/usr/bin/env python3

"""script scGammaDetector.py

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
from phypidaq.DisplayPoissonEvent import DisplayPoissonEvent
from phypidaq.helpers import DAQwait
from phypidaq.mplhelpers import run_controlGUI


def keyboard_input(cmd_queue):
    """Read keyboard input and send to Qeueu, runing as background-thread to avoid blocking"""

    while active:
        cmd = input()
        cmd_queue.put(cmd)
        if cmd == "E":
            break


def showFlash(mpQ, interval):
    """Background process to show Poisson event as a flashing circle and waveform

    relies on class DisplayPoissionEvent
    """
    flasher = DisplayPoissonEvent(mpQ, interval=interval)
    flasher()


def showOsci(mpQ, confdict):
    """Background process to show oscillogram

    relies on class DisplayPoissionEvent
    """
    scosci = scOsciDisplay(mpQ, confdict)
    scosci()


def runDAQ():
    """run data acquistion as thread"""
    count = 0
    t_start = time.time()
    t_lastupd = t_start
    osc_wait_time = 0.1
    maxADC = np.float32(display_range)
    ppFactor = 1.0 + overshoot_fraction
    while active:
        try:
            # get data
            _d = scO()
            if _d is None:  # end of daq
                break
            # got valid data
            now = time.time()
            t_evt = now - t_start
            trg_count, trg_idx, data = _d
            #
            # find signal around trigger point
            slen = 100  # length of sample around signal
            if trg_idx is not None:
                it = slen // 2  # trigger point
                i0 = max(trg_idx - it, 0)
                i1 = min(trg_idx + (slen - it), len(data[0]))
                _l = i1 - i0
                if _l < slen:
                    if i0 == 0:
                        i1 += slen - _l
                        it += slen - _l
                    else:
                        i0 -= slen - _l
                        it -= slen - _l
                signal_data = np.float32(data[0][i0:i1])
                # peak-to-peak pulse height
                mx = max(signal_data[it:])
                mn = min(signal_data[it:])
                pp_height = mx - mn
                # filter on bi-polar pulse characteristics
                if trgFalling:
                    if pp_height < ppFactor * abs(mn):
                        continue
                else:
                    if pp_height < ppFactor * abs(mx):
                        continue
            else:
                signal_data = None
                pp_height = -1
            #
            # event is accepted, proceed
            count += 1
            if showevents:
                if signal_data is not None:
                    if flasherQ.empty():
                        flasherQ.put((t_evt, signal_data / maxADC))
                else:
                    if flasherQ.empty():
                        flasherQ.put(t_evt)

            # save to file
            if csvfile is not None:
                print(f"{count}, {t_evt}, {pp_height}", file=csvfile)
                if count % 5:
                    csvfile.flush()
            # show oscillogram of raw wave form
            if showosci and osciProc.is_alive():
                if (now - t_lastupd) > osc_wait_time and osciQ.empty():
                    t_lastupd = now
                    osciQ.put(_d)
        except Exception:
            # ignore occasional errors
            pass
    # signal end to background processes by sening None
    if showevents:
        flasherQ.put(-1)
    if showosci:
        osciQ.put(None)


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        # On Windows calling this function is necessary.
        mp.freeze_support()

    kbd_control = False
    gui_control = True

    # parse command line arguments
    parser = argparse.ArgumentParser(description="Read waveforms from soundcard and display and optionally store data")
    parser.add_argument("-q", "--quiet", action="store_true", help="no status output to terminal")
    parser.add_argument("-o", "--oscilloscope", action="store_true", help="oscilloscope display")
    parser.add_argument("-n", "--noeventdisplay", action="store_true", help="deactivate event display")
    parser.add_argument("-f", "--file", type=str, default="", help="base filename to store results")
    parser.add_argument("-t", "--time", type=int, default=3600, help="run time in seconds")
    #
    # sound card sampling parameters
    parser.add_argument("-z", "--samplesize", type=int, default=1024, help="number of samples per read")
    parser.add_argument(
        "-s",
        "--samplingrate",
        type=int,
        choices={44100, 48000, 96000, 192000},
        default=44100,
        help="sampling rate",
    )
    parser.add_argument("-c", "--channels", type=int, choices={1, 2}, default=1, help="number of channels")
    # trigger settings
    parser.add_argument("-l", "--trglevel", type=float, default=5000, help="level of trigger")
    parser.add_argument("--trgfalling", action="store_true", help="trigger falling edge")
    parser.add_argument("-d", "--trgdeactivate", action="store_true", help="deactivate triggering")
    #
    # double-pulse characteristics
    parser.add_argument("--overshoot", type=float, default=0.25, help="minimum overshoot fraction")
    #
    parser.add_argument("-r", "--range", type=float, default=2**14, help="display range")
    parser.add_argument("-i", "--interval", type=float, default=30.0, help="time bin for rate display")
    #
    args = parser.parse_args()
    # - parameters to control the scrpt
    quiet = args.quiet
    showosci = args.oscilloscope
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
    overshoot_fraction = args.overshoot
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
        "overshoot_fraction": overshoot_fraction,
    }

    csvfile = None
    if filename != "":
        timestamp = time.strftime("%y%m%d-%H%M", time.localtime())
        fn = filename + "_" + timestamp + ".csv"
        csvfile = open(fn, "w")
        csvfile.write("event_numer, event_time[s], pp_height[adc]\n")

    # initialze sound card interface
    scO = SoundCardOsci(confdict=confd)
    scO.init()
    # background process to show event in real-time as "flash"
    flaherQ = None
    if showevents:
        flasherQ = mp.SimpleQueue()
        flasherProc = mp.Process(
            name="Event",
            target=showFlash,
            args=(flasherQ, interval),
        )
        flasherProc.start()
    # process to display wave forms
    osciQ = None
    if showosci:
        osciQ = mp.SimpleQueue()
        osciProc = mp.Process(
            name="Waveform",
            target=showOsci,
            args=(osciQ, confd),
        )
        osciProc.start()

    # set-up command queue
    active = True
    cmdQ = mp.SimpleQueue()  # Queue for command input from keyboard

    # set up control, eihther keyboard, GUI or both
    if kbd_control:
        kbdthread = threading.Thread(name="kbdInput", target=keyboard_input, args=(cmdQ,))
        kbdthread.start()
    if gui_control:
        # define dict for up to 8 buttons, key=name, values = [position, command]
        button_dict = {"End": [7, "E"]}
        statQ = mp.Queue()
        guiProc = mp.Process(
            name="ControlGUI", target=run_controlGUI, args=(cmdQ, "Gamma Detector DAQ", statQ, button_dict)
        )
        guiProc.start()

    # start data acquisition loop
    wait_time = 1.0
    wait = DAQwait(wait_time)
    n0 = 0
    t_start = time.time()
    t0 = t_start
    runtime = 0.0
    print("\n --> start reading from Soundcard ... ")
    osciThread = threading.Thread(target=runDAQ, args=(), daemon=True)
    osciThread.start()
    if showevents and not flasherProc.is_alive():
        print("!!! failed to start event display")
    try:
        # daq loop
        while runtime < run_seconds:
            if not cmdQ.empty():
                cmd = cmdQ.get()
                if cmd == "E":
                    break  # end cleanly
            # check for termination of subprocess windows:
            if gui_control and not guiProc.is_alive():
                print("!!! GUI control window closed - ending")
                break
            if showevents and not flasherProc.is_alive():
                print("!!! Event display closed - ending")
                break
            #
            wait()
            #
            # calculate trigger rate and update status display line
            count = scO.event_count
            t_now = time.time()  # time stamp
            runtime = t_now - t_start
            rate = (count - n0) / (t_now - t0)
            n0 = count
            t0 = t_now
            status_txt = f"active: {runtime:.1f} s  triggers: {count}  rate: {rate:.1f} Hz"
            if kbd_control:
                print(status_txt + "   -> type 'E' to end", 10 * " ", end="\r")  #
            if gui_control:
                statQ.put(status_txt)
        # -- end while
        print("\n               ... stop reading data")
    except KeyboardInterrupt:
        print("\n" + " !!! keyboard interrupt - ending ...")
    finally:
        if runtime >= run_seconds:
            input(30 * " " + "Runtime ended - type <ret> to close graphics windows -> ")
        active = False
        scO.close()  # stop reading soundcard
        if csvfile is not None:
            csvfile.close()
        time.sleep(0.9)
        if showevents and flasherProc.is_alive():
            print("terminating event display")
            flasherProc.terminate()
        if showosci and osciProc.is_alive():
            print("terminating oscilloscope display")
            osciProc.terminate()
        if gui_control and guiProc.is_alive():
            guiProc.terminate()
        sys.exit("normal end, type <ret>")
