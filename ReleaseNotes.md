# Release notes for PhyPiDAQ

## v1.1.0 (Planned)

Date (planned): 14. March 2022

### Changes

- Refactoring of the documentation
- Made `phypidaq` a Python package
- Updates to install script for an easier setup
- Support for websockets was added, enabling data transfer over networks.
- Updates to user interface, including icons and resizing behaviour
- Introduction of a resource file
- `tkinter` was completely refactored to a Qt implementation.
- Implementation of the BME680 including examples and a script for setting up the sensor
- Security Fix: Shell injection
- BMP085 and BMP180 have been declared **legacy implementations**.

## v1.0.2

Date: 14. August 2021

### Changes

- Changed driver for the INA219 implementation
- Moved the doc and images to the phypidaq folder

## v1.0.1

Date: 11 June 2021

### Changes

- Moved the folder with the images for the user interface to /resources/images
- Fixed invalid image path
- Removed non-existing module BMP180Config in `__init__.py`

## v1.0dev

### Changes

- Improvements to graphical user interface
- Support for MLX90393 magnetic field sensor
- Added description of hardware (preamplifiers)
- Support for ADC on Raspberry Pi Grove Base Hat

## v0.9.4beta

Date: June 2019

### Changes

- added output to fifo

## v0.9.3beta

Date: Jun 2019

### Changes

- Refactored timing - now controlled from main program
- Added support for GDK101 gamma ray detector
- Support for 18 channel spectral sensor AS7265x
- Support for MMA8452 accelerometer
- Added display of charging/discharging a capacitor to student course
- Generalized support for distance sensor: VL53L1X and VL53L0X

## v0.9.3dev0

### Changes

- Added possibility to replay saved data, capacitor as demo
- Added ReplayConfig.py to inject data from file
- Added distance sensor VL53L1X

## v0.9.2 Patch 2

### Changes

- Added RGB sensor TCS24725 and color sensor AS7262
- Added ToyDataConfig to test/debug without hardware
- Refactoring of `phypi.py` and `run_phypi.py` most of the code now in subdirectory `phypidaq/`

## v0.9.2 Patch 1

### Changes

- Added script `GPIO-In-Out.py`

## v0.9.2

Date: 13. February 2019

### Changes

- Some fixes of small problems
- Added simple display functionality (with minimal configuration)

## v0.9.1 Patch 2

### Changes

- Start of data acquisition in paused mode
- Added picoscope installation libraries and script `installlibs.sh`
- Support for INA219 current sensor
- Documented all `*.daq` Files
- Made sure channel information in DataLogger and DataGraphs are initialised
- Added option `xyPlots` to DataLogger and DataGraphs to select XY-Plots
- Number of formulae in `run_phypi` now may exceed number of hardware channels
- Added DiodenKennlinie.daq to record I(U) diagrams of three LEDs

## v0.9.1 Patch 1

### Changes

- Support for MMA8451 accelerometer
- Added support for temperature and pressure sensor BMP180
- Improved error messages

## v0.9.1

Date: 24. November 2018

### Changes

- Improved documentation
- Latest versions  of dependencies
- Added digital temperature sensor DS18B20
- Support for PS2204A,
- User install script

## v0.9.0

Date: 7. October 2018

Initial release
