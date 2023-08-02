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

A list of all programs, classes, configuration files and examples can be found in the document *PackageStructure.md*.
