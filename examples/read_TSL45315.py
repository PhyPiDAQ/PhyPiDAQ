import numpy as np

from phypidaq.TSL45315Config import *

# Create a config dictionary, to print all four channels
config_dict = {}

device = TSL45315Config(config_dict=config_dict)

# Initialize the device
device.init()

# Reserve space for data
data = np.array([0.])

print("Starting measuring!")

# read-out interval in s
dt = 0.5
# start time
T0 = time.time()

# Readout loop
while True:
    device.acquireData(data)
    dT = time.time() - T0
    print(f"{dT}s, {data[0]} lux")
    time.sleep(dt)
