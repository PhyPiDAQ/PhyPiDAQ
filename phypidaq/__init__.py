"""

.. moduleauthor:: Guenter Quast <guenter.quast@online.de>

.. module PhyPiDAQ
   :synopsis: data acquisition and analysis with Raspberry Pi

.. moduleauthor:: Guenter Quast <g.quast@kit.edu>

**phypidaq**
    *data acquisition and analysis with Raspberry Pi for Physics*

    a collection of tools to acquire data from hardware devices
    and to display and analyze data
"""

# Import version info
from ._version_info import *

# and set version
__version__ = _version_info._get_version_string()

# Import components to be callable at package level
__all__ = [
    "helpers",
    "Display",
    "DataLogger",
    "DataRecorder",
    "DataGraphs",
    "DataSpectrum",
    "ReplayConfig",
    "ToyDataConfig",
    "PSConfig",
    "MCP3x08Config",
    "ADS1115Config",
    "groveADCConfig",
    "GPIOCount",
    "HX711Config",
    "MAX31865Config",
    "DS18B20Config",
    "INA219Config",
    "MAX31855Config",
    "BMPx80Config",
    "MMA8451Config",
    "VL53LxConfig",
    "TCS34725Config",
    "AS7262Config",
    "AS7265xConfig",
    "GDK101Config",
    "MLX90393Config",
    "BME280Config",
    "BMP280Config",
    "BME680Config",
    "BMP388Config",
    "TSL45315Config",
    "RC10xConfig",
    "DataSpectrum",
    "DisplayPoissonEvent",
    "PL1000Config",
    "soundcardOsci",
]
