from phypidaq.TelematicsConfig import *
import time
import numpy as np

# Create a device
device = TelematicsConfig(confdict={"ip_address": "127.0.0.1"})

# Initialize the device
device.init()

# reserve space for data (four channels here)
data = np.array([0.])

print(' starting readout,     type <ctrl-C> to stop')

# read-out interval in s
dt = 1.
# start time
T0 = time.time()

# readout loop, stop with <ctrl>-C
while True:
    device.acquireData(data)
    dT = time.time() - T0
    print('%.2g, %.9g' % (dT, data[0]))
    time.sleep(dt)
