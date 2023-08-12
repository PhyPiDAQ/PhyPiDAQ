"""Driver for RadiaCode 101/102 gamma spectrometer

   relies on library *radiacode* by Maxim Andreev,

   https://github.com/cdump/radiacode

   needs pyhon dependecy and packaging tool poetry.
   Installation of package radiacode:

     > `pip3 install poetry`
     > `pip3 install radiacode`

   RETURNS:

     - counts if NChannels == 1
     - counts and dose if NChannels == 2
     - 1204 channel differential spectrum if show_spectrum

"""

import sys
import numpy as np
from radiacode import RadiaCode

cname = "RC10xConfig"


class RC10xConfig:
    """CsJ(Tl) Gamma Detector RadiaCode 101/102"""

    def __init__(self, confdict=None):
        # initialize device and set default parameters
        self.confdict = {} if confdict is None else confdict

        self.BT_mac = None if "bluetooth_mac" not in self.confdict else self.confdict["bluetooth_mac"]
        self.reset = True if "reset" not in self.confdict else self.confdict["reset"]

        try:
            self.rc = RadiaCode(bluetooth_mac=self.BT_mac)
        except Exception as e:
            print("Exception: ", e)
            sys.exit(" !!! error !!!   failed to setup device")

        self.show_spectrum = False if "show_spectrum" not in self.confdict else self.confdict["show_spectrum"]

        # number of spectrum channels is 1024 fixed
        self.NBins = 1024
        if self.show_spectrum:
            # full spectrum requested
            self.NChannels = self.NBins
            self.ChanUnits = ["#"]
            self.ChanNams = ["counts"]
            self.ChanLims = [[0, 100]]
            # displaying a spectrum needs extara data for x-axis
            self.xName = "Energy"
            self.xUnit = "keV"
        else:
            # only count rate and dose from deposited Energy
            self.NChannels = 2
            self.ChanUnits = [" ", "µGy/h"]
            self.ChanNams = ["counts", "dose", "entries"]
            self.ChanLims = [[0.0, 30.0], [0.0, 30.0 / 60.0]]

        # some constants
        rho_CsJ = 4.51  # density of CsJ in g/cm^3
        m_sensor = rho_CsJ * 1e-3  # Volume is 1 cm^3, mass in kg
        keV2J = 1.602e-16
        self.depE2dose = keV2J * 3600 * 1e6 / m_sensor  # dose rate in µGy/h

        # RC102 delivers accumulated counts, prepare array for previous readings
        self.counts0 = np.zeros(self.NBins)

        # pre-initialize calibration constants
        self.Channels = np.asarray(range(self.NBins)) + 0.5
        self.Chan2E = [-5.7, 2.38, 0.00048]
        self.BinCenters = (
            self.Chan2E[0] + self.Chan2E[1] * self.Channels + self.Chan2E[2] * self.Channels * self.Channels
        )

    def init(self):
        """Initialize device and data processing"""

        # set device configuration
        sound_on = False if "sound" not in self.confdict else self.confdict["sound"]
        self.rc.set_sound_on(sound_on)
        vibro_on = False if "vibro" not in self.confdict else self.confdict["vibro"]
        self.rc.set_vibro_on(vibro_on)
        if self.reset:
            self.rc.spectrum_reset()
            self.rc.dose_reset()

        # get calibration constants from device
        self.Channels = np.asarray(range(self.NBins)) + 0.5
        self.Chan2E = self.rc.energy_calib()
        self.BinCenters = (
            self.Chan2E[0] + self.Chan2E[1] * self.Channels + self.Chan2E[2] * self.Channels * self.Channels
        )

    def acquireData(self, buf):
        """provide data in user-supplied buffer"""

        # read spectrum data from device (counts since last call)
        cumulated_counts = np.asarray(self.rc.spectrum().counts)
        counts = cumulated_counts - self.counts0
        self.counts0 = cumulated_counts
        # number of counts
        Ncounts = np.sum(counts)
        # dose in µGy/h = µJ/(kg*h)
        deposited_energy = np.sum(counts * self.BinCenters)  # in keV
        dose = deposited_energy * self.depE2dose
        # deliver data
        if self.show_spectrum:
            buf[:] = counts
        else:
            buf[0] = Ncounts
            if self.NChannels > 1:
                buf[1] = dose

    def closeDevice(self):
        """disconnect device"""
        # noting to do ...
