import time
import numpy as np
import matplotlib.pyplot as plt


class DataSpectrum(object):
    """Display data as a spectrum (for histogram data)"""

    def __init__(self, ConfDict):
        """Args:  ConfDict: configuration dictionary"""

        # get relevant settings from PhyPiConfDict
        self.dT = ConfDict["Interval"]
        self.NChan = ConfDict["NChannels"]
        self.ChanLim = ConfDict["ChanLimits"]
        Nc = self.NChan
        self.ChanNams = [""] * self.NChan
        if "ChanNams" in ConfDict:
            v = ConfDict["ChanNams"]
            self.ChanNams[0 : min(len(v), Nc)] = v[0 : min(len(v), Nc)]
        C2V = ConfDict["Chan2Val"]
        self.a0 = C2V[0]
        self.a1 = C2V[1]
        self.a2 = C2V[2]
        self.Channels = np.asarray(range(self.NChan)) + 0.5
        self.xValues = self.Chan2Val(self.Channels)
        self.xUnit = ConfDict["xUnit"]

        self.ymax = 1.0e5
        self.ymax_diff = 5.0

        self.cumulative_counts = np.zeros(self.NChan)

        self.graphs_initialized = False

    def Chan2Val(self, C):
        # convert Channel number to Energy
        #  E = a0 + a1*C + a2 C^2
        return self.a0 + self.a1 * C + self.a2 * C * C

    def Val2Chan(self, E):
        # convert Energies to Channel Numbers
        # inverse E = a0 + a1*C + a2 C^2
        c = self.a0 - E
        return (np.sqrt(self.a1**2 - 4 * self.a2 * c) - self.a1) / (2 * self.a2)

    def initgraph(self):
        fig = plt.figure("Gamma Spectrum", figsize=(5.0, 6.0))
        fig.suptitle("Spectrum " + time.asctime(), size="large", color="b")
        fig.subplots_adjust(left=0.12, bottom=0.1, right=0.95, top=0.85, wspace=None, hspace=0.03)
        gs = fig.add_gridspec(nrows=4, ncols=1)
        # define subplots
        self.axE = fig.add_subplot(gs[:-1, :])
        self.axE.set_ylabel("Cumulative counts", size="large")
        self.axE.set_xlim(0.0, self.xValues[1023])
        self.axE.set_ylim(0.5, self.ymax)
        plt.locator_params(axis="x", nbins=12)
        self.axE.set_xticklabels([])  # no labels
        self.axE.grid(linestyle="dotted", which="both")
        self.axE.set_yscale("log")
        # a second x-axis for channels
        self.axC = self.axE.secondary_xaxis("top", functions=(self.Val2Chan, self.Chan2Val))
        self.axC.set_xlabel("Channel #")
        # define subplots
        self.axEdiff = fig.add_subplot(gs[-1, :])
        self.axEdiff.set_xlabel("Energy (keV)", size="large")
        self.axEdiff.set_ylabel("Rate", size="large")
        self.axEdiff.set_xlim(0.0, self.xValues[1023])
        self.axEdiff.set_ylim(0.0, self.ymax_diff)
        plt.locator_params(axis="x", nbins=12)
        self.axEdiff.grid(linestyle="dotted", which="both")

        self.fig = fig
        self.graphs_initialized = True

    def init(self):
        if not self.graphs_initialized:
            self.initgraph()  # create matplotlib figure
        # initialize objects to be animated
        (self.line,) = self.axE.plot([1], [0.5])
        self.line.set_xdata(self.xValues)
        (self.line_diff,) = self.axEdiff.plot([1], [0.5])
        self.line_diff.set_xdata(self.xValues)

        self.animtxtE = self.axE.text(
            0.66,
            0.9,
            "     ",
            transform=self.axE.transAxes,
            color="darkblue",
            # backgroundcolor='white',
            alpha=0.7,
        )
        self.animtxt_diff = self.axEdiff.text(
            0.66,
            0.66,
            "   diff  ",
            transform=self.axEdiff.transAxes,
            color="darkblue",
            # backgroundcolor='white', alpha=0.7,
        )
        return (self.line, self.line_diff, self.animtxtE, self.animtxt_diff)

    def __call__(self, data):
        if data is not None:
            n, dat = data
            # add data to histogram
            self.cumulative_counts += dat
            self.line.set_ydata(self.cumulative_counts)
            self.line_diff.set_ydata(dat)
            rate = np.sum(dat) / self.dT
            Ntot = np.sum(self.cumulative_counts)
            Sum_x = np.sum(self.cumulative_counts * self.xValues)
            sum_x = np.sum(dat * self.xValues) / self.dT
            self.animtxtE.set_text(f"#: {Ntot:.5g} \n" + f"$\\Sigma_x$:  {Sum_x:.4g} {self.xUnit}")
            self.animtxt_diff.set_text(f"rate:   {rate:.3g} Hz\n" + f"$\\Sigma_x$:  {sum_x:.4g} {self.xUnit}/s")
        return (self.line, self.line_diff, self.animtxtE, self.animtxt_diff)
