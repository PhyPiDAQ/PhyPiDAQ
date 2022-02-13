# PhyPiDAQ Description of Software

[Software Guide](Documentation_en.md). 

[Dikumentation der Software](Dokumentation_de.md). 

## Summary

The PhyPiDAQ project aims to provide students access to state-of-the-art measurement technology and data acquisition
tools. As it is based on standardized protocols and hardware, it can not only be cheaper to set up than similar offers
but also give a great educational introduction in methods of modern science. Additionally, the measuring technology
can be run off a power bank, making it portable and allowing great experiments in nature. This project targets students
from middle school up to undergraduates at the university level with great matching educational concepts. Looking beyond
school it is also an amazing base for STEM based competitions like
"[Jugend forscht](https://www.jugend-forscht.de/information-in-english.html)" or science fairs.

This is the software package for data acquisition and its documentation. For details, see the [detailed Documentation](Documentation_en.md). 

If you are looking for hardware guides, build
instructions or educational concepts, please check out our other [repositories](https://github.com/PhyPiDAQ).


## Übersicht in Deutscher Sprache

Das PhyPiDAQ-Projekt zielt darauf ab, Studierenden und SchülerInnen Zugang zu modernster Messtechnik und Datenerfassung
zu verschaffen. Da es auf offenen, standardisierten Protokollen und leicht verfügbarer Hardware basiert, kann es
nicht nur kostengünstig eingerichtet werden, sondern bietet auch eine hervorragende pädagogische Einführung in die
Messmethoden der modernen Wissenschaft. Die Messtechnik kann mit einer Powerbank betrieben werden, was sie tragbar macht
und Experimente auch in freier Natur ermöglicht. *PhyPiDAQ* richtet sich an SchülerInnen von der Mittelstufe bis hin zu
Studierenden auf Universitätsebene. Über die Schule hinaus ist es auch eine gute Basis für MINT-Wettbewerbe wie
"[Jugend forscht](https://www.jugend-forscht.de/)".

Dies ist das Softwarepaket zur Datenerfassung und die zugehörige Dokumentation. Weitere Information zu Installation,
Funktionsweise und Konfiguration der Software zum PhyPiDAQ-Projekt findet sich [hier](Dokumentation_de.md). 

Wenn Sie nach Hardware-Beschreibungen, Bauanleitungen oder Beschreibungen von
Experimenten mit PhyPiDAQ suchen, schauen Sie sich bitte unsere anderen
[Repositories](https://github.com/PhyPiDAQ) an.


## Quickstart

This is a quickstart guide on how to install the software package and run the demo.
The following requirements need to be met to work

- Linux/Unix operating system
- Python3.6 runtime or newer
- `git`-package installed
- If you want to use the sensor, you need a Raspberry Pi

1. Open a terminal and go to the folder, where the software should be installed.
2. Download the latest release using the following command

   ```shell
     git clone https://github.com/PhyPiDAQ/PhyPiDAQ
   ```

3. Now we need to install all required dependencies. Access the folder and execute the `installlibs.sh`. During the
   installation process you will be promoted, if you want to install the sensor drivers. They are not required to run
   the demo, but helpful for further use. As some drivers work exclusively on the Raspberry Pi, we recommend answering
   it only with `Y` if you are running on a Raspberry Pi and with `n` in all other cases.
   Additionally, you will be asked if you want to install the PicoScope drivers, where you need to enter a `Y` for yes
   or `n` for no.

   ```shell
     cd PhyPiDAQ
     ./installlibs.sh
   ```

4. Run the demo by starting the `run_phypi.py`. It will start the application and replay some recorded data in a window,
   as specified in the `PhyPiDemo.daq`.

   ```shell
     ./run_phypi.py
   ```

For further information on the installation process, additional sensor support and multiuser support refer to the
sections below.

## Supported sensors

This is a brief summary of all sensors, that are currently supported. Next to the sensors you can find a very simple
list of dimensions, that can be measured. For more information

List of actively supported sensors

- ADS1115 4 channel, 16 bit Analog-to-Digital Converter
- MCP3009 10 bit Analog-to-Digital Converter
- MCP3208 12 bit Analog-to-Digital Converter
- Grove Base Hat for RPi, 12 bit ADC
- INA219 current, voltage and power
- DS18B20 digital temperature sensor
- BME280 temperature, pressure, altitude, relative_humidity
- BME680 temperature, pressure, altitude, relative_humidity; resistance proportional to VOC particle amount
- BMP280 temperature, pressure, altitude
- MAX31865 temperature, resistance
- MAX31855 converter for thermocouple
- MAX31856 converter for PT100 temperature sensor
- MMA8451 accelerometer
- MLX90393 magnetometer
- TCS34752 RGB sensor
- AS7262Config 6 channel color sensor
- AS7265x 18 channel spectral sensor
- VL53L0X and VL53L1X distance sensors
- GDK101 gamma-ray detector
- PicoScope USB oscilloscopes
- rate measurements via GPIO pins

Legacy support

- BMP085 temperature, pressure
- BMP180 temperature, pressure

## Contributing

For information on how to contribute to this project, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the `MIT BSD 2-Clause License`. For more information refer to the [LICENSE](LICENSE)
file.
