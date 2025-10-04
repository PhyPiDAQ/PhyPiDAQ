# PhyPiDAQ Description of Software

[Software Guide](docs/Documentation_en.md).

[Dokumentation der Software](docs/Dokumentation_de.md).

## Summary

The PhyPiDAQ project aims to provide students access to state-of-the-art measurement technology and data acquisition
tools. As it is based on standardized protocols and hardware, it can not only be cheaper to set up than similar offers
but also give a great educational introduction in methods of modern science. Additionally, the measuring technology
can be run off a power bank, making it portable and allowing great experiments in nature. This project targets students
from middle school up to undergraduates at the university level with great matching educational concepts. Looking beyond
school it is also an amazing base for STEM based competitions like
"[Jugend forscht](https://www.jugend-forscht.de/information-in-english.html)" or science fairs.

This is the software package for data acquisition and its documentation. For details, see the
[full Documentation](docs/Documentation_en.md).

If you are looking for hardware guides, build instructions or educational concepts, please check out our other
[repositories](https://github.com/PhyPiDAQ).

### Currently available Documentation

- [Software Description](https://github.com/PhyPiDAQ/PhyPiDAQ/blob/main/docs/Documentation_en.md)
- [Educators Guide](https://github.com/PhyPiDAQ/EducatorsGuide/blob/main/EducatorsGuide.md)
- [Hardware build instructions](https://github.com/PhyPiDAQ/MeasuringCase/blob/main/Documentation_en.md)

## Übersicht in deutscher Sprache

Das PhyPiDAQ-Projekt zielt darauf ab, Studierenden und SchülerInnen Zugang zu modernster Messtechnik und Datenerfassung
zu verschaffen. Da es auf offenen, standardisierten Protokollen und leicht verfügbarer Hardware basiert, kann es
nicht nur kostengünstig eingerichtet werden, sondern bietet auch eine hervorragende pädagogische Einführung in die
Messmethoden der modernen Wissenschaft. Die Messtechnik kann mit einer Powerbank betrieben werden, was sie tragbar macht
und Experimente auch in freier Natur ermöglicht. *PhyPiDAQ* richtet sich an SchülerInnen von der Mittelstufe bis hin zu
Studierenden auf Universitätsebene. Über die Schule hinaus ist es auch eine gute Basis für MINT-Wettbewerbe wie
"[Jugend forscht](https://www.jugend-forscht.de/)".

Dies ist das Softwarepaket zur Datenerfassung und die zugehörige Dokumentation. Weitere Information zu Installation,
Funktionsweise und Konfiguration der Software zum PhyPiDAQ-Projekt findet sich [hier](docs/Dokumentation_de.md).

Wenn Sie nach Hardware-Beschreibungen, Bauanleitungen oder Beschreibungen von
Experimenten mit PhyPiDAQ suchen, schauen Sie sich bitte unsere anderen
[Repositories](https://github.com/PhyPiDAQ) an.

### Derzeit verfügbare Dokumentation

- [Anleitung für Lehrkräfte](https://github.com/PhyPiDAQ/EducatorsGuide/blob/main/Anleitung.md)
- [Beschreibung der Software](https://github.com/PhyPiDAQ/PhyPiDAQ/blob/main/docs/Dokumentation_de.md)
- [Bauanleitung Messkoffer](https://github.com/PhyPiDAQ/MeasuringCase/blob/main/Dokumentation_de.md)

## Quick-start

This is a quick-start guide on how to install the software package and run a demo.
The following requirements need to be met to work

- Linux/Unix operating system
- Python 3.7 or newer
- `git`-package installed

Installation runs on Raspberry Pi with Debian 11 (bullseye) or 12 (bookworm),
however, not all sensor libraries could be fully tested.
OS 13 (Trixie) is not yet supported!

1. Open a terminal and go to the folder where the software should be installed.
2. Download the latest release using the following command

   ```shell
     git clone https://github.com/PhyPiDAQ/PhyPiDAQ
   ```

3. Now we need to install all required dependencies. Access the folder and execute  the shell
   script `installlibs.sh`. During the installation process you will be promoted whether 
   to install the sensor drivers. They are not required to ru the demo and some applications,
  but they are required for sensors connected to the GPIO pins of the Raspberry Pi. Therefore,
  we recommend answering `y` only if needed and `n` in all other cases. Additionally, you will
  be asked if you want to install the PicoScope drivers. Answering `y`is only needed on the
  Raspberry Pi, as on other systems the libraries are installed together with the PicoScope
  Software. 

   ```shell
     cd PhyPiDAQ
     ./installlibs.sh
   ```
4. On the latest Linux version, a virtual *Python* environment is needed. For PhyPiDAQ this is
  set up and provided system-wide for every user in the directory `/usr/local/share/phypy/` by
  executing   

   ```shell
      cd PhyPiDAQ
      ./install_user.sh 
   ```

   This script also initializes a work directory in the user's home directory with local copies
   of configuration files from the install directory. On a Raspberry Pi,  desktop icons are
   also created.   
   
   It is also necessary to activate the virtual *Python* environment at every login by executing  
   
     ```shell
       cd 
       source activate_phypy.sh
     ```
  If exclusive use of PhyPiDAQ is foreseen on a system, the command for activation can also
  be included in the users `.bashrc` file. 
   
5. Now everything is ready to run the PhyPiDAQ demo by either typing `phypi.py` or by
  double-clicking the `phypi_demo`icon.    
  This starts the application to replay some recorded data in a window, as specified in the configuration file `PhyPiDemo.daq`.

For further information on the installation process, on sensors and hardware needs or
on educational examples see the detailed documentation in the repositories under the
link [http://github.com/PhyPiDAQ](http://github.com/PhyPiDAQ).


## Supported sensors

This is a brief summary of all sensors currently supported. Next to the sensors there
is a list of quantities measured by each sensor.

### List of actively supported sensors

- ADS1115 4 channel, 16 bit Analog-to-Digital Converter
- MCP3009 10 bit Analog-to-Digital Converter
- MCP3208 12 bit Analog-to-Digital Converter
- Grove Base Hat for RPi, 12 bit ADC
- INA219 current, voltage and power
- DS18B20 digital temperature sensor
- BME280 temperature, pressure, altitude, relative_humidity
- BME680 temperature, pressure, altitude, relative_humidity; resistance proportional to VOC particle amount
- BMP280 temperature, pressure, altitude
- BMP388 temperature, pressure, altitude
- MAX31855 converter for thermocouple
- MAX31865 temperature, resistance (used for PT100 and PT1000 temperature sensor)
- MMA8451 accelerometer
- MLX90393 magnetometer
- TCS34752 RGB sensor
- AS7262Config 6 channel color sensor
- AS7265x 18 channel spectral sensor
- VL53L0X and VL53L1X distance sensors
- TSL45315 Luminance sensor
- GDK101 gamma-ray detector
- PicoScope USB oscilloscopes
- PicoLog 100 Sereis USB data loggers
- rate measurements via GPIO pins
- wave form recording from soundcard

### Legacy support

- BMP085 temperature, pressure
- BMP180 temperature, pressure

## Contributing

For information on how to contribute to this project, please refer to the
[CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the `MIT BSD 2-Clause License`. For more information
refer to the [LICENSE](LICENSE) file.
