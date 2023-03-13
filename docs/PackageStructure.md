# Structure of the phypidaq

## Programs

- `run_phypi.py`  
    run data acquisition and display modules as specified in configuration files (default `PhyPiConf.daq`
    and *.yaml* files ins subdirectory *config/*)
- `phypi.py`  
    graphical user interface to edit configuration files and start the script `run_phypi.py`

## Modules

- `phypidaq/__init__.py`  
   initialisation for package *phypidaq*

- `phypidaq/_version_info.py`  
    version info for package *phypidaq*

- `phypidaq/ADS1115Config.py`  
    class for handling of analog-to-digital converter ADS1115

- `phypidaq/MCP3008Config.py`  
    class analog-to-digital converter MCP3008

- `phypidaq/MCP3008Config.py`  
    class for current and voltage sensor INA219

- `phypidaq/DS18B20Config.py`  
    class for handling of digital thermometer DS18B20

- ``phypidaq/BMPx80Config.py``  
    class for the digital temperature and pressure sensors BMP180/280 or BME280

- ``phypidaq/MMA8451Config.py``  
    class for the digital accelerometer MMA8451

- `phypidaq/GPIOCount.py`  
    class for reading rates from GPIO pins

- `phypidaq/MAX31855Config.py`  
    class for MAX31855 thermocouple-to-digital converter

- `phypidaq/MAX31865Config.py`  
    class for MAX31865 resistance-to-digital converter

- `phypidaq/PSConfig.py`  
    class for PicoScope USB oscilloscopes

- `phypidaq/VL53LxConfig`  
    class for VL53L1X distance sensor

- `phypidaq/TCS34725Config`
    class for TCS34725 RGB color sensor

- `phypidaq/AS7262Config`
    class for AS7262 six channel color sensor

- `phypidaq/AS7265xConfig`
    class for AS7265x 18 channel spectral sensor

- `phypidaq/GDK101Config.py`  
    class for gamma ray detektor GDK101, FTLAB

- `phypidaq/ToyDataConfig.py`  
    class to generate simulated data (for test, debugging or exercises)

- `phypidaq/ReplayConfig`  
    class to replay data from file

- `phypidaq/Display`  
    interface and background-process handling data visualisation

- `phypidaq/DataLogge`  
    class for display of data histories and xy diagrams

- `phypidaq/DataGraph`  
    general display module for data as bar graphs, history plots and xy-graphs

- `phypidaq/DataRecorde`  
    store data in CSV format

- `phypidaq/pulseGPIO`
    class to set or pulse GPIO pin of raspberry py

- `phypidaq/runPhyPiDAQ`  
    class for script `run_phypi.py`

- `phypidaq/runPhyPiUI.py`
    class for graphical user interface `phypi.py`, uses `phypiUI` as base class

- `phypidaq/phypyUI`

    base class for `runPhyPyUI`, generated from `phypi.ui` with `pyuic5`

- `phypidaq/phypi.ui`
    output of `designer-qt5` , describes the graphical user interface

## Configuration files

- `phypidaq.cfg`  
     global configuration for directory with configuration files and initial work directory;
     if this file is found in the `home` directory, it takes priority over the one in the installation directory
- `PhyPiConf.daq`  
     main configuration file, depends on device configurations in sub-directory *config/*
- `config/ADS1115Config.yaml` 16 bit ADC
- `config/MCP3008Config.yaml` 10 bit ADC
- `config/MCP3208Config.yaml`  12 bit ADC
- `config/INA219Config.yaml` current and voltage sensor
- `config/DS18B20Config.yaml` digital temperature sensor
- `config/BMP280Config.yaml` temperature and pressure sensor
- `config/BMP180Config.yaml` temperature and pressure sensor
- `config/GPIOCount.yaml`  frequency measurement via GPIO pin
- `config/MAX31855Config.yaml` converter for thermocouple
- `config/MAX31865Config.yaml` converter for PT-100
- `config/INA219Config.yaml` current-voltage sensor
- `config/TCS34752Config.yaml` RGB sensor
- `config/AS7262Config.yaml` 6 channel color sensor
- `config/AS7265xConfig.yaml` 18 channel spectral sensor
- `config/VL53L1XConfig.yaml` distance sensor
- `config/GDK101.yaml` gamma-ray detector
- `config/PSConfig.yaml`  PicoScope usb oscilloscope

## Examples

- `examples/read_analog.py`  
    very minimalist example to read one channel from an analog-to-ditigal converter

- ``examples/display_analog.py``  
    very minimalist example to read one channel from an analog-to-ditigal converter and
    display data as a history graph

- ``examples/display_analog2.py``  
    read two channels from an analog-to-ditigal converter and
    display data as a history graph

- `examples/read_INA210.py`  
    read data from INA219 current and voltage sensor

- ``examples/read_18B20.py``s
     simple example to read the temperature sensor DS18B20

- ``examples/readBMPx80.py``
    simple example to read the digital temperature  and pressure sensor BMP180/280

- ``examples/readMMA8541.py``
    simple example to read the digital accelerometer MMA8451

- `examples/runOsci.py`  
    run an oscilloscope display, configuration as specified in *.yaml* file (default is `PSOsci.yaml`)

- `examples/GPIO-In-Out.py`  
    example to control  GPIO pins: generate square signal on output pin from variable voltage on input pin

- `examples/poissonLED.py`  
    generate a random signal following Poisson statistics on a GPIO pin

- `examples/FreqGen.py`  
    generate a fixed frequency signal on a GPIO pin  

- `examples/set_MPC4725`  
    example to set voltage on MCP4725 digital-to-analog converter

## Configuration files for *run_phypi.py*

- `examples/Amperemeter.daq`  
    display current and eventually voltage read from INA219 sensor
- ``examples/Barometer.daq``  
    uses BMB180 or BMP280 sensors to display temperature and air pressure
- ``examples/Accelerometer.daq``  
    uses MMA8451 to display x-, y- and z-acceleration
- ``examples/NoiseMeter.daq``  
    measure noise with a microphone connected to PicoScope USB oscilloscope;
     displays the *rms* of 200 samples taken over a time periods of 20 ms.
    Can also be used with geophone SM-24
- `examples/RGBsensor.daq`
    RGB color sensor
- `examples/ColorSpectrum.daq`
    six channel color sensor
- `examples/AS7265x.daq`
    18 channel spectral sensor
- `examples/GammaDose.daq`  
    measurement of gamma-ray dose with GDK101
- `examples/ToyData.daq`
    generation and display of simulated data  
- `examples/ReplayData.daq`  
    data from file (for demo mode)
- `examples/readPipe.py`  
    read data from named linux pipe (*run_phypi.py* with option DAQfifo: \<pipe name\>)
