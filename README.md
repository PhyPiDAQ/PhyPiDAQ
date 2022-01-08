# PhyPiDAQ

Note: The documentation is also available in German and have the `_de` suffix.

The PhyPiDAQ project aims to provide student access to state-of-the-art measurement technology and data acquisition 
tools. As it is based on standardized protocols and hardware, it can not only be cheaper to set up than similar offers 
but also give a great educational introduction in methods of modern science. Additionally, the measuring technology 
can be run off a power bank, making it portable and allowing great experiments in nature. It targets students from 
middle school up to undergraduates at the university level with great matching educational concepts. Looking beyond 
school it is also an amazing base for STEM based competitions like 
"[Jugend forscht](https://www.jugend-forscht.de/information-in-english.html)" or science fairs.     

This is the software package for data acquisition and its documentation. If you are looking for hardware guides, build 
instructions or educational concepts, please checkout our other [repositories](https://github.com/PhyPiDAQ).

## Quickstart
This is a quickstart guide on how to install the software package and run the demo. 
The following requirements need to be met to work 
 - Linux/Unix operating system
 - Python3 runtime
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

- BME280 (temperature, pressure, altitude, relative_humidity)
- BME680 (temperature, pressure, altitude, relative_humidity; resistance proportional to VOC particle amount)
- BMP280 (temperature, pressure, altitude)
- INA219 (current, voltage and power)
- MAX31865 (temperature, resistance)

Legacy support
- BMP085 (temperature, pressure)
- BMP180 (temperature, pressure)