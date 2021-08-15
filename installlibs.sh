#!/bin/bash
#
# script to install libraries PhyPiDAQ depends on
#
# -----------------------------------------------

sudo apt-get install python3-yaml --yes
sudo apt-get install python3-scipy --yes
sudo apt-get install python3-matplotlib --yes
sudo apt-get install python3-pyqt5 --yes
sudo apt-get install libatlas-base-dev --yes # needed to build numpy

read -p "Do you want to install the sensor drivers (Y/n)?" -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
  # some python packages for IO
  sudo pip3 install i2cdev
  sudo pip3 install spidev
  sudo pip3 install pyusb
  sudo pip3 install smbus2

  sudo pip3 install installlibs/whl/*.whl # python wheels

  sudo pip3 install installlibs/tgz/*.tar.gz # python packages

  # Install all sensor drivers specified in the
  sudo pip3 install -r /requirements.txt

  sudo dpkg -i installlibs/picoscopelibs/*.deb # picoscope
  sudo usermod -a -G tty pi # grant access to USB for user pi
fi

