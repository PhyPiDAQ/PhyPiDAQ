"""module SoundCardOsci to read data from a sound card"""

import pyaudio
import time
import numpy as np
import matplotlib.pyplot as plt


class SoundCardOsci:
    """configuration and interface for reading wave forms from sound-card

    requirements: pyaudio package

    to run an example, type:

       `python3 soundcardOsci.py`


    This class reads data from one or two channels of a sound card.
    Basic trigger requirements can be activated to record only samples
    selected samples, e.g. containing a pulse occuring at random times,
    e. g. as produced by a radiation detector.
    """

    def __init__(self, confdict=None, verbose=0):
        self.verbose = verbose
        # read configuration dictionary
        self.confdict = {} if confdict is None else confdict
        self.channels = [1] if "channels" not in self.confdict else self.confdict["channels"]
        self.NSamples = 1024 if "number_of_samples" not in self.confdict else self.confdict["number_of_samples"]
        self.NChannels = len(self.channels)
        if self.verbose:
            print(f"{self.NChannels} active channels: {self.SCchannels}")
        self.sampling_rate = 44100 if "sampling_rate" not in confdict else confdict["sampling_rate"]
        # trigger config
        self.trgActive = 0 if "trgActive" not in confdict else confdict["trgActive"]
        self.trgChan = 1 if "trgChan" not in confdict else confdict["trgChan"]
        self.trgFalling = 0 if "trgFalling" not in confdict else confdict["trgFalling"]
        self.trgThreshold = 100 if "trgThreshold" not in confdict else confdict["trgThreshold"]
        # set reasonable default for format
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.maxADC = 2**15  # for 16 bit soundcard

        # create  interface to PortAudio
        self.pyaudio = pyaudio.PyAudio()

    def init(self):
        """open audio stream and initialize"""
        self.stream = self.pyaudio.open(
            format=self.sample_format,
            channels=self.NChannels,
            rate=self.sampling_rate,
            frames_per_buffer=self.NSamples,
            input=True,
        )
        # (re-)set trigger event count
        self.event_count = 0
        self.active = True

    def __call__(self):
        """read data stream and return data if trigger condition is met"""

        # read data from sound card
        _d = np.frombuffer(self.stream.read(self.NSamples), dtype=np.int16)
        data = [_d] if self.NChannels == 1 else [_d[0::2], _d[1::2]]
        # return data if in free-running mode
        if self.active and not self.trgActive:
            self.event_count += 1
            return (self.event_count, None, data)
        # else check trigger condition
        _triggered = False
        while self.active and not _triggered:
            if self.trgFalling:
                idx = np.argwhere(data[self.trgChan - 1] < self.trgThreshold)
            else:
                idx = np.argwhere(data[self.trgChan - 1] > self.trgThreshold)
            if len(idx) > 0:
                self.event_count += 1
                _triggered = True
                return (self.event_count, idx[0][0], data)
            _d = np.frombuffer(self.stream.read(self.NSamples), dtype=np.int16)
            data = [_d] if self.NChannels == 1 else [_d[0::2], _d[1::2]]
        # return None if called but not active (can be used  by clients)
        return None

    def close(self):
        self.active = False
        time.sleep(1.0)
        # Stop and close the stream
        self.stream.stop_stream()
        self.stream.close()
        # Terminate the PortAudio interface
        self.pyaudio.terminate()


class scOsciDisplay:
    """simple, animated display for sound card data

    fast blitting is used to only redraw the waveform line(s)
    """

    def __init__(self, confdict=None):
        self.confdict = {} if confdict is None else confdict
        self.channels = [1] if "channels" not in self.confdict else self.confdict["channels"]
        self.NSamples = 1024 if "number_of_samples" not in self.confdict else self.confdict["number_of_samples"]
        self.NChannels = len(self.channels)
        self.sampling_rate = 44100 if "sampling_rate" not in confdict else confdict["sampling_rate"]
        self.max = 2**15 if "range" not in confdict else confdict["range"]
        # trigger config
        self.trgActive = 0 if "trgActive" not in confdict else confdict["trgActive"]
        self.trgChan = 1 if "trgChan" not in confdict else confdict["trgChan"]
        self.trgFalling = 0 if "trgFalling" not in confdict else confdict["trgFalling"]
        self.trgThreshold = 100 if "trgThreshold" not in confdict else confdict["trgThreshold"]
        # create a figure
        self.fig = plt.figure("Audio", figsize=(8.0, 6.0))
        self.fig.suptitle("sound card data")
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.15, bottom=0.12, right=0.98, top=0.90, wspace=None, hspace=0.1)  #
        self.ax.grid(linestyle="dotted", color="blue")
        self.ax.set_ylabel("aplitude (counts)")
        self.ax.set_xlabel("time (ms)")
        tplt = (np.linspace(0, self.NSamples, self.NSamples) + 0.5) / self.sampling_rate
        self.iStep = int(self.NSamples / 333) + 1
        (self.pline,) = self.ax.plot(tplt[:: self.iStep], np.zeros(self.NSamples)[:: self.iStep], animated=True)
        if self.NChannels == 2:
            (self.pline2,) = self.ax.plot(
                tplt[:: self.iStep],
                np.zeros(self.NSamples)[:: self.iStep],
                animated=True,
            )
        if self.trgFalling:
            mx = 1.0
            mn = 0.5 * (1 + self.trgThreshold / self.max)
        else:
            mn = 0.0
            mx = 0.5 * (1 + self.trgThreshold / self.max)
        self.trgline = self.ax.axvline(0.0, ymin=mn, ymax=mx, color="red", linestyle="dashed", animated=True)
        self.ax.set_ylim(-self.max, self.max)
        # plt.ion()
        plt.show(block=False)
        plt.pause(0.1)
        self.bg = self.fig.canvas.copy_from_bbox(self.fig.bbox)
        self.ax.draw_artist(self.pline)
        if self.NChannels == 2:
            self.ax.draw_artist(self.pline2)
        self.ax.draw_artist(self.trgline)

    def __call__(self, data, trg_idx=None):
        # update line data and redraw
        self.fig.canvas.restore_region(self.bg)
        self.pline.set_ydata(data[0][:: self.iStep])
        self.ax.draw_artist(self.pline)
        if self.NChannels == 2:
            self.pline2.set_ydata(data[1][:: self.iStep])
            self.ax.draw_artist(self.pline2)
        if trg_idx is not None:
            self.trgline.set_xdata(trg_idx / self.sampling_rate)
            self.ax.draw_artist(self.trgline)
        self.fig.canvas.blit(self.fig.bbox)
        self.fig.canvas.flush_events()


if __name__ == "__main__":  # ------------------------------
    # application example for SoundCardOsci

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
