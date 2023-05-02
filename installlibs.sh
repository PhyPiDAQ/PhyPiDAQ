#!/bin/bash
#
# script to install libraries PhyPiDAQ depends on
#
# -----------------------------------------------

# Print info message
echo "Starting installation of PhyPiDAQ"

# Update package indices
sudo apt update

# Install base packages
sudo apt install python3-yaml --yes
sudo apt install python3-scipy --yes
sudo apt install python3-matplotlib --yes
sudo apt install python3-pyqt5 --yes
sudo apt install libatlas-base-dev --yes # needed to build numpy

# install this package (phypidaq) 
sudo pip3 install .

while true; do
    read -p "Do you wish to install sensor drivers (y/n)? " yn
    case $yn in
        [Yy]* ) echo "Installing drivers";
          # some python packages for IO
          sudo pip3 install i2cdev;
          sudo pip3 install spidev;
          sudo pip3 install pyusb;
          sudo pip3 install smbus2;

          sudo pip3 install installlibs/whl/*.whl; # python wheels

          # Install all sensor drivers specified in the
          sudo pip3 install -r requirements.txt;

          sudo usermod -a -G tty $USER; # grant access to USB for the current user

          break;;
        [Nn]* ) echo "Skipping sensor driver installation"; break;;
        * ) echo "Please answer yes or no.";;
    esac
done

while true; do
    read -p "Do you wish to install the PicoScope drivers? " yn
    case $yn in
        [Yy]* ) echo "Installing PicoScope drivers";
          sudo dpkg -i installlibs/picoscopelibs/*.deb; # picoscope
          sudo usermod -a -G tty $USER; # grant access to USB for the current user
          break;;
        [Nn]* ) echo "Skipping PicoScope driver installation"; break;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo "Installation finished! Enjoy the usage of PhyPiDAQ"
