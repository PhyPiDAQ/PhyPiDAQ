"""helper functions"""

import os
import errno
import time
from scipy import interpolate
# for controlGUI


def generateCalibrationFunction(calibd):
    """
    interpolate calibration table t= true, r = raw values ;
    if only one number for trueVals given, then this is
    interpreted as a simple calibration factor

    Args:
      calibd:   calibration data
          either a single number as calibration factor: fc
          or a list or two arrays: [ [true values], [raw values] ]
    Returns: interpolation function
    """
    try:
        iter(calibd)
        # if no error, input is an array
        r = calibd[1]
        t = calibd[0]
    except TypeError:
        # input is only one number
        r = [0.0, 1.0]
        t = [0.0, calibd]
        # check input
    if len(t) != len(r):
        print("!!! generateCalibrationFunction: lengths of input arrays not equal - exiting")
        exit(1)
    # make sure raw values are sorted - and simultaneously sort true values
    r, t = zip(*sorted(zip(r, t)))
    # perform spline interpolation of appropriate order k
    return interpolate.UnivariateSpline(r, t, k=min(3, len(t) - 1), s=0)


def stop_processes(process_list):
    """
    Close all running processes at end of run
    """
    for p in process_list:  # stop all sub-processes
        if p.is_alive():
            print("    terminating " + p.name)
            if p.is_alive():
                p.terminate()
            time.sleep(1.0)


def keyboard_wait(prompt=None):
    """wait for keyboard input"""
    #  wait for input
    if prompt is None:
        return input(50 * " " + "type <ret> to exit -> ")
    else:
        return input(prompt)


class DAQwait(object):
    """class implementing sleep corrected with system time"""

    def __init__(self, dt):
        """Args:
        dt: wait time in seconds
        """
        self.dt = dt
        self.lag = False  # indicate occurrence of time lag
        self.T0 = time.time()

    def __call__(self, T0=None):
        """guarantee correct timing
        Args:
          TO:   start time of action to be timed
                  if not given, take end-time of last wait
        """
        if T0 is not None:
            self.T0 = T0
        dtcor = self.dt - time.time() + self.T0
        if dtcor > 0.0:
            time.sleep(dtcor)
            self.lag = False
        else:
            self.lag = True
        self.T0 = time.time()  # end of sleep = start of next interval


class RingBuffer(object):
    """ring buffer to store N objects"""

    # implemented as a simple list, where old entries
    #  are overwritten if length of list is exceeded

    def __init__(self, N):
        """
        N: size of buffer
        """
        self.N = N
        self.B = [None] * N  # initialize a list
        self.full = False
        self.k = -1

    def store(self, d):
        """
        d: data object
        """

        # increment index, eventually overwrite oldest data
        self.k += 1
        if self.k == self.N:
            self.k = 0
            self.full = True
        # store data
        self.B[self.k] = d

    def read(self):
        """return all data"""

        if self.full:
            return self.B[self.k :] + self.B[: self.k]
        else:
            return self.B[: self.k]


class FifoManager(object):
    """open a fifo (linux pipe) to transfer data to external process"""

    def __init__(self, fname):
        """open fifo
        fname: name of fifo
        """

        try:
            os.mkfifo(fname)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("!!! failed to open fifi !!!")
                print(e)
                raise

        self.fifo = open(fname, "w", 1)

    def __call__(self, d):
        print(d, end="", file=self.fifo)

    def close(self):
        self.fifo.close()
