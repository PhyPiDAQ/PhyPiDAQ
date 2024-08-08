import sys
import numpy as np
from scipy.special import loggamma
from scipy.optimize import newton
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

mpl.use("Qt5Agg")
plt.style.use("dark_background")  # dark canvas background


# helper function (fromPhyPraKit.phyFit)
def Poisson_CI(lam, sigma=1.0):
    """
    determine one-sigma Confidence Interval around the
    mean lambda of a Poisson distribution, Poiss(x, lambda).

    The method is based on delta-log-Likelihood (dlL)
    of the Poission likelihood

    Args:
     - lam: mean of Poission distribution
     - sigma: z-Value (number of equivalent Gaussian sigma) of desired confidence level
    """

    # helper functions
    def nlLPoisson(x, lam):
        """negative log-likelihood of Poissoin distribution"""
        return lam - x * np.log(lam) + loggamma(x + 1.0)

    def f(x, lam, dlL):
        """Delta log-L - offset, input to Newton method"""
        return nlLPoisson(x, lam) - nlLPoisson(lam, lam) - dlL

    dlL = 0.5 * sigma * sigma
    # for dlL=0.5, there is only one intersection with zero for lam<1.8
    dl = 1.3 * np.sqrt(lam)
    dlm = min(dl, lam)
    cp = newton(f, x0=lam + dl, x1=lam, args=(lam, dlL))
    try:  # may not converge for small lambda, as there is no intersection < lam
        cm = newton(f, x0=lam - dlm, x1=lam, args=(lam, dlL))
    except Exception:
        cm = 0.0
    if (cp - cm) < lam / 100.0:  # found same intersection,
        cm = 0.0  # set 1st one to 0.
    return cm, cp


class DisplayPoissonEvent:
    """display a short flash when data is transferred via queue,
    corresponding to a single Poisson event

        Args:

          -  mpQ: multiprocessing queue for input
          -  rate: generated rate for Poisson process
          -  mean: desired expected mean / bin
          -  interval: bin width for history plot if not derived from rate and mean
    """

    def __init__(self, mpQ, rate=None, mean=None, interval=None):
        """specify either rate and mean or interval"""
        self.mpQ = mpQ  # queue for data
        self.rate = rate  # average event rate
        self.mean = mean  # desired mean value for time bin
        if rate is not None:
            self.tau = 1.0 / rate  # average time between events
            self.tflash = max(self.tau / 20, 0.050) if self.tau < 1.0 else 0.01  # flash duration
            self.interval = self.mean / self.rate  # bin width
        #       self.flash_color = '#ffff80' # yellowish
        elif interval is not None:
            self.tflash = 0.01  # flash duration
            self.interval = interval  # bin width
        else:
            sys.exit("!!! DisplayPoissonEvent: input error - either rate and mean or inerval must be given")
        if self.interval <= 20:
            time_unit = "s"
            self.unit_factor = 1.0
        else:
            time_unit = "min"
            self.unit_factor = 1.0 / 60.0
        self.title_color = "goldenrod"
        self.flash_color = "#AFCFFF"  # blueish
        self.bg_color = "black"

        # initialize an (interactive) figure
        if rate is not None:
            self.fig = plt.figure("PoissonFlash 𝜏=%.3g" % (self.tau), figsize=(6.0, 8.0))
        else:
            self.fig = plt.figure("EventFlash", figsize=(6.0, 8.0))
        self.fig.canvas.mpl_connect("close_event", self.on_mpl_window_closed)
        self.mpl_active = True
        if self.interval is None:
            self.fig.suptitle("Poisson Statistics", size="x-large", color=self.title_color)
        else:
            self.fig.suptitle("Event Display", size="x-large", color=self.title_color)
        self.fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.95, wspace=None, hspace=0.15)
        gs = self.fig.add_gridspec(nrows=4, ncols=1)
        # 1st graph for "Poisson Flash"
        self.ax = self.fig.add_subplot(gs[:-1, :])
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)
        # plt.axis("off")
        self.ax.xaxis.set_tick_params(labelbottom=False)
        self.ax.yaxis.set_tick_params(labelleft=False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        c = patches.Circle((0, 0.0), 1, fc=self.bg_color, ec="orange")
        c1 = patches.Circle((0, 0.0), 1, ec="#4F4F4F", lw=20)
        c2 = patches.Circle((0, 0.0), 1.1, ec="#2F2F2F", lw=60)
        c3 = patches.Circle((0, 0.0), 1.4, ec="#1F1F1F", lw=20)
        self.flashobj = self.ax.add_patch(c3)  # body of detector
        self.flashobj = self.ax.add_patch(c2)  # body of detector
        self.flashobj = self.ax.add_patch(c1)  # border
        self.flashobj = self.ax.add_patch(c)  # light-emitting surface
        #  add a graph
        self.flashxplt = np.linspace(-1.0, 1.0, 100)
        (self.flashline,) = self.ax.plot(self.flashxplt, 100 * [None])
        # add rate value from generator input
        if rate is not None:
            _ = self.ax.text(
                0.05,
                0.96,
                "Event Rate: %.2f Hz" % (self.rate),
                transform=self.ax.transAxes,
                color="yellow",
            )
        self.txt = self.ax.text(0.05, 0.92, " ", transform=self.ax.transAxes, color="azure")
        #
        # 2nd graph for rate history
        self.axrate = self.fig.add_subplot(gs[-1, :])
        self.Npoints = 150
        self.xmin = -self.interval * self.Npoints
        self.xmax = 0.0
        self.axrate.set_xlim(self.xmin * self.unit_factor, self.xmax)
        self.ymin = 0.0
        if self.mean is not None:
            self.ymax = self.mean + 5 * np.sqrt(self.mean)  # 5 sigma range
        else:
            self.ymax = 3
        self.axrate.set_ylim(self.ymin, self.ymax)
        self.axrate.grid(True, alpha=0.5)
        self.axrate.set_xlabel(f"History ({time_unit}) ")
        self.axrate.set_ylabel("Counts")
        if self.mean is not None and self.rate is not None:
            _ = self.axrate.text(
                0.02,
                0.88,
                r"$\Delta$t=%2gs  $\Rightarrow$  mean=%.2f" % (self.mean / self.rate, self.mean),
                transform=self.axrate.transAxes,
                color="orangered",
            )
            self.axrate.axhline(self.mean, color="red", linestyle="dashed")
            if self.mean > 1.5:
                z_value = 1.0
                cm1, cp1 = Poisson_CI(self.mean, sigma=z_value)  # 68%  confidence intervall
                rect1 = patches.Rectangle(
                    (self.xmin, cm1),
                    self.xmax - self.xmin,
                    cp1 - cm1,
                    color="green",
                    alpha=0.5,
                )
                self.axrate.add_patch(rect1)
            if self.mean > 10:
                cm2, cp2 = Poisson_CI(self.mean, 2.0)  # 96%  confidence intervall
                rect2 = patches.Rectangle(
                    (self.xmin, cm2),
                    self.xmax - self.xmin,
                    cp2 - cm2,
                    color="yellow",
                    alpha=0.5,
                )
                self.axrate.add_patch(rect2)

        self.xplt = np.linspace(-self.Npoints * self.interval * self.unit_factor, 0.0, self.Npoints)
        self.counts = np.zeros(self.Npoints) - 0.1
        (self.hline,) = self.axrate.plot(
            self.xplt,
            self.Npoints * [None],
            ".--",
            lw=1,
            markersize=6,
            color="ivory",
            mec="orange",
        )
        plt.ion()
        plt.show()
        # draw initial graph
        self.fig.canvas.start_event_loop(0.5 * self.tflash)

    def on_mpl_window_closed(self, ax):
        # detect when matplotlib window is closed
        self.mpl_active = False

    def __call__(self):
        """Flash object

        Data via input queu mpQ: time and, optionally, waveform data

          flashpulse:  wave form data with 100 samples normalised to one

        """

        flashpulse = None
        N = 0
        lastbin = 0
        self.counts[0] = 0
        max_y = 3
        t_last = 0.
        rate = 0.
        while self.mpl_active:
            # wait for data, avoid blocking
            if self.mpQ.empty():
                self.fig.canvas.start_event_loop(0.005)
                continue
            else:
                _d = self.mpQ.get()
                if isinstance(_d, tuple):
                    t = _d[0]
                    flashpulse = _d[1]
                else:
                    t = _d

            if t >= 0:
                # show colored object ("flash")
                t_last = t
                self.flashline.set_ydata(100 * [None])
                self.flashobj.set_facecolor(self.flash_color)
                self.fig.canvas.start_event_loop(0.5 * self.tflash)
                # replaces plt.pause() without stealing focus
                # collect statistics
                N += 1
                rate = N / t if N > 2 else 0.0
                status_text = "active %.1f s" % t + 15 * " " + "counts %d" % N + 5 * " " + "average rate %.3f Hz" % rate
                # display statistics and make flash object invisible again
                self.txt.set_text(status_text)
                self.flashobj.set_facecolor(self.bg_color)
                if flashpulse is not None:
                    self.flashline.set_ydata(flashpulse)
                self.fig.canvas.start_event_loop(0.5 * self.tflash)
                # calculate entries for rate histogram
                hbin = int(t / self.interval) % self.Npoints
                if hbin != lastbin:
                    k = lastbin % self.Npoints
                    self.hline.set_ydata(np.concatenate((self.counts[k + 1:], self.counts[: k + 1])))
                    if self.counts[lastbin] > max_y:
                        max_y = self.counts[lastbin]
                        self.axrate.set_ylim(0.0, max_y + 0.1)
                    lastbin = hbin
                    self.counts[hbin] = 0  # initialize counter for next bin
                if self.counts[hbin] < 0:
                    self.counts[hbin] = 0
                self.counts[hbin] += 1
            else:
                print("\n*==* DisplayPoissonEvent exiting ...")
                print(
                    8 * " "
                    + "active %.1f s" % t_last
                    + 5 * " "
                    + "counts %d" % N
                    + 5 * " "
                    + "average rate %.3f Hz" % rate
                )
                break


def showFlash(mpQ, rate, mean):
    """Background process to show Poisson event as a flashing circle

    relies on class DisPlayPoissionEvent
    """
    flasher = DisplayPoissonEvent(mpQ, rate=rate, mean=mean)
    flasher()
