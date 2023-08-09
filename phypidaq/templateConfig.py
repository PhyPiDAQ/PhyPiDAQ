# This example illustrates the general structure of a PhyPiDAQ driver


"""PhyPiDAQ Driver for ????

   general information on purpose of device, 
   needed packages and their installation on raspberry pi

"""

import ???


cname = '???Config'


class ???Config(object):
    """ ??? descriptoin"""

    def __init__(confdict=None):
        # establish communication with device here
        # force exit on error
                # number of spectrum channels is 1024 fixed

        # set number of returned channels, units, names and ranges
        self.NChannels = *
        self.ChanUnits = [?, ?, ...]
        self.ChanNams =  [?, ?, ...]
        self.ChanLims = [ [?, ?], [?, ?], ...]
  
    def init(self):
        """Initialize special features of device"""

    def acquireData(self, buf):
        """provide data in user-supplied buffer"""

        # buf = ...
       
    def closeDevide(self):
        """disconnect device"""
        pass
