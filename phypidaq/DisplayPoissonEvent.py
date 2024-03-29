import numpy as np
import time
from scipy.special import loggamma
from scipy.optimize import newton
import matplotlib as mpl

mpl.use('Qt5Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.style.use('dark_background')  # dark canvas background


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
    except:
        cm = 0.0
    if (cp - cm) < lam / 100.0:  # found same intersection,
        cm = 0.0  #  set 1st one to 0.
    return cm, cp


class DisplayPoissonEvent:
    """display a short flash when data is transferred via queue,
    corresponding to a single Poisson event

    Args:

      - mpQ: queue for input data
      - rate: average event rate
      - mean: desired mean (defines length of time interval for event counts)
    """

    def __init__(self, mpQ, rate=1.0, mean=4.0):
        self.mpQ = mpQ  # queue for data
        self.rate = rate  # average event rate
        self.tau = 1.0 / rate  # average time between events
        self.mean = mean  # desired mean value for time bin

        self.tflash = max(self.tau / 20, 0.050)  # flash time for object indicating event occurance
        #       self.flash_color = '#ffff80' # yellowish
        self.title_color = "goldenrod"
        self.flash_color = '#AFCFFF'  # blueish
        self.bg_color = 'black'

        # initialize an (interactive) figure
        self.fig = plt.figure("PoissonFlash 𝜏=%.3g" % (self.tau), figsize=(6.0, 8.0))
        self.fig.canvas.mpl_connect('close_event', self.on_mpl_window_closed)
        self.mpl_active = True
        self.fig.suptitle('Poisson Statistics', size='x-large', color=self.title_color)
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
        self.flashobj = self.ax.add_patch(c)  # light-emitting survface
        _ = self.ax.text(0.05, 0.96, "Event Rate: %.2f Hz" % (self.rate), transform=self.ax.transAxes, color='yellow')
        self.txt = self.ax.text(0.05, 0.92, " ", transform=self.ax.transAxes, color='azure')
        # 2nd graph for rate history
        self.axrate = self.fig.add_subplot(gs[-1, :])
        self.axrate.set_ylabel("Counts")
        self.axrate.set_xlabel("History (s)")
        self.Npoints = 150
        self.interval = self.mean * self.tau  # bin width
        self.xmin = -self.interval * self.Npoints
        self.xmax = 0.0
        self.axrate.set_xlim(self.xmin, self.xmax)
        self.ymin = 0.0
        self.ymax = self.mean + 5 * np.sqrt(self.mean)  # allow for 5 sigma spread
        self.axrate.set_ylim(self.ymin, self.ymax)
        self.axrate.grid(True, alpha=0.5)
        self.axrate.set_xlabel("History [s]")
        self.axrate.set_ylabel("Counts")
        _ = self.axrate.text(
            0.02,
            0.88,
            "$\Delta$t=%2gs  $\Rightarrow$  mean=%.2f" % (self.mean / self.rate, self.mean),
            transform=self.axrate.transAxes,
            color='orangered',
        )
        self.axrate.axhline(self.mean, color='red', linestyle='dashed')
        if self.mean > 1.5:
            z_value = 1.0
            cm1, cp1 = Poisson_CI(self.mean, sigma=z_value)  # 68%  confidence intervall
            rect1 = patches.Rectangle((self.xmin, cm1), self.xmax - self.xmin, cp1 - cm1, color='green', alpha=0.5)
            self.axrate.add_patch(rect1)
        if self.mean > 10:
            cm2, cp2 = Poisson_CI(self.mean, 2.0)  # 96%  confidence intervall
            rect2 = patches.Rectangle((self.xmin, cm2), self.xmax - self.xmin, cp2 - cm2, color='yellow', alpha=0.5)
            self.axrate.add_patch(rect2)

        self.xplt = np.linspace(-self.Npoints * self.interval, 0.0, self.Npoints)
        self.counts = np.zeros(self.Npoints) - 1.0
        (self.hline,) = self.axrate.plot(self.xplt, self.counts, '.--', lw=1, markersize=6, color="ivory", mec="orange")
        plt.ion()
        plt.show()

    def on_mpl_window_closed(self, ax):
        # detect when matplotlib window is closed
        self.mpl_active = False
        
    def __call__(self):
        """Flash object"""
        N = 0
        Nlast = 0
        lastbin = 0
        T0 = time.time()
        while self.mpl_active:
            t = self.mpQ.get()
            if t >= 0:
                # show colored object
                t_last = t
                self.flashobj.set_facecolor(self.flash_color)
                self.fig.canvas.start_event_loop(0.5 * self.tflash)
                # replaces plt.pause() without stealing focus
                # collect statistics
                N += 1
                rate = N / t if N > 2 else 0.0
                status_text = "active %.1f s" % t + 15 * ' ' + "counts %d" % N + 5 * ' ' + "average rate %.3f Hz" % rate
                # display statistics and make flash object invisible
                self.txt.set_text(status_text)
                self.flashobj.set_facecolor(self.bg_color)
                self.fig.canvas.start_event_loop(0.5 * self.tflash)
                # calculate entries for rate histogram
                hbin = int(t / self.interval) % self.Npoints
                if hbin != lastbin:
                    k = lastbin % self.Npoints
                    self.hline.set_ydata(np.concatenate((self.counts[k + 1 :], self.counts[: k + 1])))
                    lastbin = hbin
                    self.counts[hbin] = 0  # initialize counter for next bin
                self.counts[hbin] += 1
            else:
                print("\n*==* Poissson Flasher exiting ...")
                print(8 * ' ' + "active %.1f s" % t_last + 5 * ' ' + "counts %d" % N + 5 * ' ' + "average rate %.3f Hz" % rate)


def showFlash(mpQ, rate, mean):
    """Background process to show Poisson event as a flashing circle

    relies on class DisPlayPoissionEvent
    """
    flasher = DisplayPoissonEvent(mpQ, rate, mean)
    flasher()
