#!/bin/bash
#
# script to install libraries PhyPiDAQ depends on
#
#       requires a Python virtual environment 
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
sudo apt install libatlas-base-dev --yes  # needed to build numpy
sudo apt install libglib2.0-dev --yes  # needed for bluepy
sudo apt install portaudio19-dev --yes  # for pyaudio

# check for virtual python environment and create if not present
PHYPYENV="/usr/local/share/phypy"
if [ -d "$PHYPYENV" ];
    then
      echo "installing in virtual environment $PHYPYENV"
    else
      echo "creating Python virtual environment in directory $PHYPYENV"
      sudo mkdir $PHYPYENV
      sudo chown $USER $PHYPYENV
      sudo chmod a+rwx $PHYPYENV  # would be better to use separate group phypi
      python3 -m venv "$PHYPYENV" --system-site-packages 

fi
# activate virtual environment
source "$PHYPYENV"/bin/activate

# install this package (phypidaq) 
python -m pip install .

while true; do
    read -p "Do you wish to install sensor drivers (y/n)? " yn
    case $yn in
        [Yy]* ) echo "Installing drivers";
          # some python packages for IO
          python -m pip install i2cdev;
          python -m pip install spidev;
          python -m pip install pyusb;
          python -m pip install smbus2;

          python -m pip install installlibs/whl/*.whl; # python wheels

          # Install all sensor drivers specified in the
          python -m pip install -r requirements.txt;

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
