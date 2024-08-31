#!/usr/bin/python
"""PoissonLED
LED flashing according to a random Poisson Process
"""

from __future__ import print_function, division, unicode_literals
from __future__ import absolute_import

import time
import sys
import math
import random
import threading
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)


def flash_led(pin, deltatime):
    # flash GPIO pin for time dt
    gpio.output(pin, 1)
    time.sleep(deltatime)
    gpio.output(pin, 0)


pLED = 26
gpio.setup(pLED, gpio.OUT)

tau = 1.0  # 1 second default
if len(sys.argv) > 1:
    tau = float(sys.argv[1])
tflash = 0.0075

print("flashing GPIO pin %i randomly with tau= %.3gs" % (pLED, tau))
try:
    dtcum = 0.0
    T0 = time.time()
    while True:
        flashThread = threading.Thread(
            target=flash_led,
            args=(
                pLED,
                tflash,
            ),
        )
        flashThread.start()
        # generate exponentially distributed waiting time
        dt = -tau * math.log(random.uniform(0.0, 1.0))
        dtcor = dt - time.time() + T0 + dtcum
        if dtcor > 0.0:
            time.sleep(dtcor)
        dtcum += dt

except KeyboardInterrupt:
    print("keyboard interrupt - ending")

finally:
    gpio.cleanup()
    sys.exit(0)
