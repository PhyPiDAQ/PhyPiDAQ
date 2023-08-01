# Structure of the PhyPiDAQ package

The structure of the code is deliberately kept very minimalistic and simple, owing to the pedagogical nature
of the project. Sensors are supported by wrapper classes with a unique and simple interface; using these classes
to configure and read out a sensor follows a very straight-forward scheme, illustrated here for a sensor named
*SENSOR*:

```
### PhyPiDAQ example script 

# import phypidaq module supporting SENSOR
  from phypidaq.SENSORConfig import * 

# create an instance of the class to control the device
device = SENSORConfig()

# initialize the device
device.init()

# reserve space to data (here one channel only)
dat =np.array([0.])

print(' starting readout,     type <ctrl-C> to stop')

# read-out interval in s
dt = 1.
# start time
T0 = time.time()

# readout loop, stop with <ctrl>-C
while True:
      device.acquireData(dat)
      dT = time.time() - T0
      print('%.2g, %.4g' % (dT, dat))
      time.sleep(dt)

```

Configuration parameters needed by the sensors are defined as reasonable defaults and can be
overwritten by a sensor-specific configuration file in *yaml*-format that is passed to the *SENSORconfig*
class when an instance is created. 

A typical sensor class looks like follows:

``` 
# Class SENSORConfig

class SENSORConfig(object):

    def __init__(self, config_dict = None):
         # set default configuration or read from configuration dictionary 
         config_dict = {} if config_dict is None else config_dict
        
         # set up sensor parameters, e.g. I2C address, options etc.
        
        ...   

         # set some of the default properties needed to 
         self.NCHannels = ?
         self.ChanLims = [[?,?], ...]
         self.ChanNams = ['?', ... ]
         self.ChanUnits = ['?', ... ]


    def init(self):
        # set-up the sensor, usually by calling the driver class provided by  the vendor 
        self.sensor = ???()
        
        
    def acquireData(self, buf):
        # read data from sensor and copy to buffer
        buf[0] = self.sensor.x()
        if self.NChannels > 1:
            buf[2] = self.sensor.y()
        ... 
        
     def close(self):
       # disconnect  sensor (may not be needed, but it is wise to provide this functionality)   
          pass
          
 ``` 
 
Note that sensor-specific interactions with the sensor-driver only occur in the methods `init()` and `acquireData()`.
The interface for the user is very light-weight, and most of the complexity of a given sensor is shielded by the 
parameters and options defined in the configuration file. Even complex sensors can thus be easily mastered
by beginners.  

In the simple example above, recorded data were simply displayed on the terminal. The *PhyPiDAQ* also offers
modules to display data in real-time as bar-graph, history plot or as a 2d-representation for pairs of (x,y) data. 
In many cases, an extension of the simple template of the user program shown above will do the job. In addition
to the sensor, a display method must be initialised and called after acquisition of data. No *time.sleep(dt)*  is
necessary in this case, as the display module also takes care of the proper waiting time.  

```
        ...
        
# create an instance of device and display ...
device = SENSORConfig()
display = Display(interval=0.1)
# ... and initialize
device.init()
display.init()

print(' starting readout,     type <ctrl-C> to stop')
# start time
T0 = time.time()
try:
    # readout loop, stop with <ctrl>-C
    while True:
        device.acquireData(dat)
        dT = time.time() - T0
        print('%.1f, %.4g' % (dT, dat))
        display.show(dat)
except KeyboardInterrupt:
    print('ctrl-C received - ending')
    device.closeDevice()
    display.close()

``` 

For many use cases, writing dedicated own code is not practical. Therefore, a stand-alone program is provided, *run_phypi.py*.
It is driven by global configuration files in *yaml*-format wir the ending *.daq* and sensor configuration files. A graphical interface, *phypy.py*, is also provided. It loads the configurations, contains an editor function to modify and store them, and
then starts *run_phypy.py*. These programs are described in detail in the *EducatorsGuide*; details about the configuration
files are given in the *Software Guide*.  

A list of all programs, classes, configuration files and examples is listed in the following sub-sections. 

### Programs

- `run_phypi.py`  
    run data acquisition and display modules as specified in configuration files (default `PhyPiConf.daq`
    and *.yaml* files ins subdirectory *config/*)
- `phypi.py`  
    graphical user interface to edit configuration files and start the script `run_phypi.py`

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
- `config/GDK101.yaml` gamma-ray detector
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
- `examples/config_files/ToyData.daq`
    generation and display of simulated data  
- `examples/config_files/ReplayData.daq`
    data from file (for demo mode)
