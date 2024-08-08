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
from phypidaq.helpers import DAQwait
from phypidaq.DisplayPoissonEvent import DisplayPoissonEvent

# for contrilGUI
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

mpl.use("Qt5Agg")
plt.style.use("dark_background")  # dark canvas background


def keyboard_input(cmd_queue):
    """Read keyboard input and send to Qeueu, runing as background-thread to avoid blocking"""

    while active:
        cmd = input()
        cmd_queue.put(cmd)
        if cmd == "E":
            break


class controlGUI:
    """graphical user interface to control apps via multirocessing Queue

    Args:

      - cmdQ: a multiprocesing Queue to accept commands
      - appName: name of app to be controlled
      - statQ: mp Queue to show status data
      - confdict: a configuration dictionary for commands (not yer implemented)
    """

    def __init__(self, cmdQ, appName="TestApp", statQ=None, confdict=None):
        self.cmdQ = cmdQ
        self.statQ = statQ
        self.cdict = {} if confdict is None else confdict

        self.mpl_active = True
        self.interval = 100  # update for timer

        # create a figure
        self.f = plt.figure("control Gui", figsize=(6, 1.5))
        self.f.canvas.mpl_connect("close_event", self.on_mpl_window_closed)

        self.f.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.95, wspace=None, hspace=0.15)
        gs = self.f.add_gridspec(nrows=5, ncols=1)
        # 1st subplot for text
        self.ax0 = self.f.add_subplot(gs[:-2, :])
        # no axes or labels
        self.ax0.xaxis.set_tick_params(labelbottom=False)
        self.ax0.yaxis.set_tick_params(labelleft=False)
        self.ax0.set_xticks([])
        self.ax0.set_yticks([])
        self.ax0.text(0.1, 0.5, f"control {appName}", color="goldenrod", size=15)
        self.status_txt = self.ax0.text(0.05, 0.075, "active:          ")

    # call-back functions
    def on_mpl_window_closed(self, ax):
        # active when application window is closed
        self.mpl_active = False
        self.cmdQ.put("E")
        time.sleep(0.3)
        sys.exit(0)

    def cb_end(self, event):
        # active when application window is closed
        self.mpl_active = False
        self.cmdQ.put("E")
        time.sleep(0.3)
        sys.exit(0)

    def cb_b1(self, event):
        print("button 1", event)

    def cb_b2(self, event):
        print("button 2", event)

    def update(self, ax):
        """called by timern"""
        if not self.statQ.empty():
            self.status_txt.set_text(self.statQ.get())
        ax.figure.canvas.draw()

    def run(self):
        """run the GUI"""
        # define widgets
        b1_text = "but_1"
        b2_text = "but_2"
        # create commad buttons
        # - end button
        abend = self.f.add_axes([0.9, 0.05, 0.08, 0.16])
        bend = Button(abend, "End", color="darkred", hovercolor="0.5")
        bend.on_clicked(self.cb_end)
        # - more buttons
        ab1 = self.f.add_axes([0.1, 0.05, 0.08, 0.16])
        b1 = Button(ab1, b1_text, color="0.25", hovercolor="0.5")
        b1.on_clicked(self.cb_b1)
        ab2 = self.f.add_axes([0.2, 0.05, 0.08, 0.16])
        b2 = Button(ab2, b2_text, color="0.25", hovercolor="0.5")
        b2.on_clicked(self.cb_b2)

        timer = self.f.canvas.new_timer(interval=self.interval)
        timer.add_callback(self.update, self.ax0)
        self.t_start = time.time()
        timer.start()

        print("sarting event loop - click 'end' to stop")
        plt.show()


def run_controlGUI(*args, **kwargs):
    gui = controlGUI(*args, **kwargs)
    gui.run()


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
    t_start = time.time()
    t_lastupd = t_start
    osc_wait_time = 0.1
    maxADC = np.float32(display_range)
    while active:
        try:
            # get data
            _d = scO()
            if _d is None:  # end of daq
                break
            count, trg_idx, data = _d
            #
            # find data around signal
            if trg_idx is not None:
                i0 = max(trg_idx - 25, 0)
                i1 = min(trg_idx + 75, len(data[0]))
                d = i1 - i0
                if d < 100:
                    if i0 == 0:
                        i1 += 100 - d
                    else:
                        i0 -= 100 - d
                signal_data = np.float32(data[0][i0:i1])
            else:
                signal_data = None
            #
            # calculate pulse height
            if signal_data is not None:
                pulse_height = max(signal_data) - min(signal_data)
            else:
                pulse_height = -1

            # save to file
            if csvfile is not None:
                print(f"{count}, {now-t_start}, {pulse_height}", file=csvfile)
                if count % 5:
                    csvfile.flush()
            # show oscillogram of raw wave form
            if showosci:
                if (now - t_lastupd) > osc_wait_time:
                    osciQ.put((trg_idx, data))
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
                    flasherQ.put((now - t_start, signal_data / maxADC))
                else:
                    flasherQ.put(now - t_start)
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

    kbd_control = True
    gui_control = True

    # parse command line arguments
    parser = argparse.ArgumentParser(description="Read waveforms from soundcard and display and optionally store data")
    parser.add_argument("-q", "--quiet", action="store_true", help="no status output to terminal")
    parser.add_argument("-o", "--oscilloscope", action="store_true", help="oscilloscope display")
    parser.add_argument("-n", "--noeventdisplay", action="store_true", help="deactivate event display")
    parser.add_argument("-f", "--file", type=str, default="", help="base filename to store results")
    parser.add_argument("-t", "--time", type=int, default=3600, help="run time in seconds")
    #
    parser.add_argument(
        "-s",
        "--samplingrate",
        type=int,
        choices={44100, 48000, 96000, 192000},
        default=44100,
        help="sampling rate",
    )
    parser.add_argument("-c", "--channels", type=int, choices={1, 2}, default=1, help="number of channels")
    parser.add_argument("-l", "--trglevel", type=float, default=5000, help="level of trigger")
    parser.add_argument("--trgfalling", action="store_true", help="trigger falling edge")
    parser.add_argument("-d", "--trgdeactivate", action="store_true", help="deactivate triggering")
    parser.add_argument("-z", "--samplesize", type=int, default=1024, help="number of samples per read")
    parser.add_argument("-r", "--range", type=float, default=2**14, help="display range")
    #
    parser.add_argument("-i", "--interval", type=float, default=30.0, help="time bin for rate    display")
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
        csvfile.write("event_numer, event_time[s], pulse_height[adc]\n")

    # initialze sound card interface
    scO = SoundCardOsci(confdict=confd)
    scO.init()
    # background process to show event in real-time as "flash"
    flaherQ = None
    if showevents:
        flasherQ = mp.Queue()
        flasherProc = mp.Process(
            name="Event",
            target=showFlash,
            args=(flasherQ, interval),
        )
        flasherProc.start()
    # process to display wave forms
    osciQ = None
    if showosci:
        osciQ = mp.Queue()
        osciProc = mp.Process(
            name="Waveform",
            target=showOsci,
            args=(osciQ, confd),
        )
        osciProc.start()

    # set-up command queue
    active = True
    cmdQ = mp.Queue()  # Queue for command input from keyboard

    # set up control, eihther keyboard, GUI or both
    if kbd_control:
        kbdthread = threading.Thread(name="kbdInput", target=keyboard_input, args=(cmdQ,))
        kbdthread.start()
    if gui_control:
        statQ = mp.Queue()
        guiProc = mp.Process(name="ControlGUI", target=run_controlGUI, args=(cmdQ, "Gamma Detector DAQ", statQ, None))
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
            wait()
            # calculate trigger rate and update status display line
            count = scO.event_count
            now = time.time()  # time stamp
            runtime = now - t_start
            rate = (count - n0) / (now - t0)
            n0 = count
            t0 = now
            status_txt = f"active: {runtime:.1f}  triggers: {count}  rate: {rate:.1f} Hz"
            if kbd_control:
                print(status_txt + "   -> type 'E' to end", 10 * " ", end="\r")  #
            if gui_control:
                statQ.put(status_txt)
        # -- end while
        print("\n               ... stop reading data")
    except KeyboardInterrupt:
        print("\n" + " !!! keyboard interrupt - ending ...")
    finally:
        active = False
        #        input(30 * " " + "Finished !  Type <ret> to exit -> ")
        scO.close()  # stop reading soundcard
        if csvfile is not None:
            csvfile.close()
        time.sleep(0.3)
        if showevents and flasherProc.is_alive():
            print("terminating event display")
            flasherProc.terminate()
        if showosci and osciProc.is_alive():
            osciProc.terminate()
        if gui_control and guiProc.is_alive():
            guiProc.terminate()
        sys.exit("normal end, type <ret>")
