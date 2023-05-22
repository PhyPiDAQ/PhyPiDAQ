# Release notes for PhyPiDAQ

All notable changes to this project will be documented in this file.

## [1.3.0] - 2023-05-22

### Added

- Documentation about `flake8` usage
- `util` submodule, starting with path logic
- More examples
  - Introduced `read_MCP3x08.py`
  - `read_MAX31855.py` example
  - `read_ADXL345.py` example

### Changed

- Implementation of the ADS1115
  - Renamed `read_analog.py` to `read_ADS1115.py`
- Implementation of MAX31855
- Implementation of the ADXL345
- `MCP4725` DAC example
- Changed scope of markdown linting to the root directory only
- Display PhyPiDAQ Version number also in display window title
- Structure of examples
  - Improved naming
  - Updated docs of the package structure
- Improved install script `installlibs.sh`
- Improved config writing error logging
- Better code documentation 

### Fixed

- Correct file path separator used on all platforms
- File path checks are os independent now
- Removed unused functions

## [1.2.1] - 2022-11-06

### Added

- Support for the TSL45315 luminance sensor

### Fixed

- Fixed wrong labeled parameter in BMP280 I2C-address config

## [1.2.0] - 2022-10-23

### Added

- Support for the BMP388 temperature sensor
- Software Version in window name

### Changed

- Desktop link files are now created dynamically by the `install_user.sh`
- Added `phypi.py` and `run_phypi.py` as package scripts

### Fixed

- Make `installlibs.sh` username independent
- Make `install_user.sh` username and installation path independent
- Typos in documentation

## [1.1.1] - 2022-03-15

### Fixed

- BME680 wasn't listed as a part of the module.

## [1.1.0] - 2022-03-13

### Added

- Support for websockets was added, enabling data transfer over networks.
- Introduction of a resource file
- Implementation of the BME680 including examples and a script for setting up the sensor

### Changed

- Refactoring of the documentation
- Made `phypidaq` a Python package
- Updates to install script for an easier setup

### Deprecated

- BMP085 and BMP180 have been declared **legacy implementations**.

### Removed

- Python 2-support has been dropped.
- `tkinter` was completely refactored to a Qt implementation.

### Fixed

- Updates to user interface, including icons and resizing behaviour

### Security

- Patched shell injection

## [1.0.2] - 2021-08-14

### Changed

- Changed driver for the INA219 implementation
- Moved the doc and images to the phypidaq folder

## [1.0.1] - 2021-06-11

### Changed

- Moved the folder with the images for the user interface to /resources/images
- Removed non-existing module BMP180Config in `__init__.py`

### Fixed

- Fixed invalid image path

## [1.0.0] - 2020-12-13

### Added

- Support for MLX90393 magnetic field sensor
- Added description of hardware (preamplifiers)
- Support for ADC on Raspberry Pi Grove Base Hat

### Changed

- Improvements to graphical user interface

## [0.9.4] - 2019-06-15

### Added

- added output to fifo

## [0.9.3] - 2019-06-01

### Added

- Added support for GDK101 gamma ray detector
- Support for 18 channel spectral sensor AS7265x
- Support for MMA8452 accelerometer
- Added display of charging/discharging a capacitor to student course
- Added possibility to replay saved data, capacitor as demo
- Added ReplayConfig.py to inject data from file
- Added distance sensor VL53L1X
- Added script `GPIO-In-Out.py`
- Added RGB sensor TCS24725 and color sensor AS7262
- Added ToyDataConfig to test/debug without hardware

### Changed

- Refactored timing - now controlled from main program
- Generalized support for distance sensor: VL53L1X and VL53L0X
- Refactoring of `phypi.py` and `run_phypi.py` most of the code now in subdirectory `phypidaq/`

## [0.9.2] - 2019-02-13

### Added

- Added simple display functionality (with minimal configuration)
- Added picoscope installation libraries and script `installlibs.sh`
- Support for INA219 current sensor
- Added option `xyPlots` to DataLogger and DataGraphs to select XY-Plots
- Number of formulae in `run_phypi` now may exceed number of hardware channels
- Added DiodenKennlinie.daq to record I(U) diagrams of three LEDs

### Changed

- Start of data acquisition in paused mode
- Documented all `*.daq` Files

### Fixed

- Made sure channel information in DataLogger and DataGraphs are initialised
- Some fixes of small problems

## [0.9.1] - 2018-11-24

### Added

- Support for MMA8451 accelerometer
- Added support for temperature and pressure sensor BMP180
- Added digital temperature sensor DS18B20
- Support for PS2204A
- User install script

### Changed

- Improved documentation
- Latest versions of dependencies
- Improved error messages

## [0.9.0] - 2018-10-07

### Added

- Initial release
