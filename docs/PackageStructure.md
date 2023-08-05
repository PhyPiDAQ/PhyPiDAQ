# Structure of the PhyPiDAQ package

The structure of the code is deliberately kept very minimalistic and simple,
owing to the pedagogical nature of the *PhyPiDAQ* project. The examples
provided as part of the package are as important as the code itself.
Related information is collected in the separate packages *EducatorsGuide*,
*MeasuringCase* and *Sensor_Documentation*.


The directory structure is as follows:

```
|--> PhyPiDAQ  |
               | --> EducatorsGuide            # general introduction for Educators
               | --> Hardware_Case             # build instructions for hardware
               | --> Sensor_Documentation      # features of supported sensors
               | --> PhyPiDAQ              |
	                                   | --> phypidaq       # code and sensor library
	                                   | --> installibs     # vendor-specific sensor libraries
					   | --> config         # sensor configuration files
                                           | --> examples       # scripts illustrating the usage
					   | --> doc            # documentation
					   | --> package installation files (.whl and .tar.gz)

```

A list of all programs, classes, configuration files and examples is listed in the following sub-sections. 


### Modules

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

- `phypidaq/RC10xConfig.py`  
    class for gamma ray spectrometer RadiaCode 101/102

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

### Configuration files

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
- `config/GDK101.yaml` FTLAB GDK101 gamma-ray detector
- `config/RC10x.yaml` RadiaCode gamma-ray spectrometer
- `config/PSConfig.yaml`  PicoScope usb oscilloscope

### Examples

- ``examples/display_analog.py``
    very minimalist example to read one channel from an analog-to-digital converter and
    display data as a history graph

- ``examples/display_analog_2_channels.py``
    read two channels from an analog-to-digital converter and display data as a history graph

- `examples/FreqGen.py`
    generate a fixed frequency signal on a GPIO pin

- `examples/GPIO-In-Out.py`
    example to control  GPIO pins: generate square signal on output pin from variable voltage on input pin

- `examples/poissonLED.py`
    generate a random signal following Poisson statistics on a GPIO pin

- ``examples/read_18B20.py``s
     simple example to read the temperature sensor DS18B20

- `examples/read_ADS1115.py`
    very minimalist example to read one channel from an analog-to-digital converter

- `examples/read_ADXL345.py`
    read data from ADXL345 accelerometer

- `examples/read_BMxx8x.py`
    read data from various Bosch BMP/BME environment sensors  

- ``examples/read_BMPx80.py``
    simple example to read the digital temperature  and pressure sensor BMP180/280 (legacy support)

- `examples/read_INA219.py`
    read data from INA219 current and voltage sensor

- `examples/read_MAX31855.py`
    read data from MAX31855 thermocouple convertor

- ``examples/read_MMA8541.py``
    simple example to read the digital accelerometer MMA8451

- `examples/read_Pipe.py`
    read data from named linux pipe (*run_phypi.py* with option DAQfifo: \<pipe name\>)

- `examples/read_test.py`
    read random generated data

- `examples/read_TSL45315.py`
    read data from TSL45315 luminance sensor

- `examples/read_Websocket.py`
    read data from websocket

- `examples/RePlot.py`
    plot saved data

- `examples/sendPipe2ws.py`
    send data from pipe to websocket

- `examples/set_MPC4725`
    example to set voltage on MCP4725 digital-to-analog converter

- `examples/oscilloscope/runOsci.py`
    run an oscilloscope display, configuration as specified in *.yaml* file (default is `PSOsci.yaml`)

- `examples/utils/burnIn_BME680.py`
    script to automatically to burn in the sensor before first usage to ensure accurate VOC data

### Configuration files for *run_phypi.py*

- `examples/config_files/Amperemeter.daq`
    display current and eventually voltage read from INA219 sensor
- ``examples/config_files/Barometer.daq``
    uses BMB180 or BMP280 sensors to display temperature and air pressure
- ``examples/config_files/Accelerometer.daq``
    uses MMA8451 to display x-, y- and z-acceleration
- ``examples/config_files/NoiseMeter.daq``
    measure noise with a microphone connected to PicoScope USB oscilloscope;
     displays the *rms* of 200 samples taken over a time periods of 20 ms.
    Can also be used with geophone SM-24
- `examples/config_files/RGBsensor.daq`
    RGB color sensor
- `examples/config_files/ColorSpectrum.daq`
    six channel color sensor
- `examples/config_files/AS7265x.daq`
    18 channel spectral sensor
- `examples/config_files/GammaDose.daq`
    measurement of gamma-ray dose with GDK101
- `examples/config_files/RC102_GammaDose.daq`
    measurement of gamma-ray dose with RadiaCode 102 gamma spectrometer
- `examples/config_files/ToyData.daq`
    generation and display of simulated data  
- `examples/config_files/ReplayData.daq`
    data from file (for demo mode)
