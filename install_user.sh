#!/bin/bash
#
# script to initially copy files to user directory ~/PhyPi/
#

# -----------------------------------------

if [ "$1" != "" ]; then
    USERDIR=$1
else
    USERDIR="PhyPi"
fi

# -----------------------------------------

# Get path of the script
SCRIPT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Set the path for the home directory
DIR=$HOME/$USERDIR
echo "copying files to "$DIR

mkdir -p $DIR

if [ -d $DIR ]; then
# enter here, if directory exists

  # Create the new desktop icons dynamically
  printf "[Desktop Entry]\nType=Application\nEncoding=UTF-8\nName=PhyPi\nComment=PhyPi Configuration\nIcon=" > $HOME/Desktop/phypi.desktop
  printf $SCRIPT_PATH >> $HOME/Desktop/phypi.desktop
  printf "/phypidaq/images/PhiPi_icon.png\nExec=lxterminal -t \"PhyPiDAQ\" -e " >> $HOME/Desktop/phypi.desktop
  printf $SCRIPT_PATH >> $HOME/Desktop/phypi.desktop
  printf "/phypi.py\nTerminal=false\n" >> $HOME/Desktop/phypi.desktop

  printf "[Desktop Entry]\nType=Application\nEncoding=UTF-8\nName=PhyPi Demo\nComment=PhyPi Configuration\nIcon=" > $HOME/Desktop/phypi_demo.desktop
  printf $SCRIPT_PATH >> $HOME/Desktop/phypi_demo.desktop
  printf "/phypidaq/images/PhiPi_icon.png\nExec=lxterminal -t \"PhyPiDAQ\" -e " >> $HOME/Desktop/phypi_demo.desktop
  printf $SCRIPT_PATH >> $HOME/Desktop/phypi_demo.desktop
  printf "/phypi.py " >> $HOME/Desktop/phypi_demo.desktop
  printf $SCRIPT_PATH >> $HOME/Desktop/phypi_demo.desktop
  printf "/PhyPiDemo.daq\nTerminal=false\n" >> $HOME/Desktop/phypi_demo.desktop

  # Ensure, that the desktop links have the correct permissions
  chmod a+x $HOME/Desktop/*.desktop

  # copy documentation
  # mkdir -p $DIR/doc
  # cp -auv doc/*.pdf $DIR/doc/
  # cp -auv README_de.pdf $DIR

  #copy python code
  cp -auv phypi.py $DIR
  cp -auv run_phypi.py $DIR
  # mkdir $DIR/phypidaq # no longer needed with new Qt set-up
  # cp -auv phypidaq/images $DIR/phypidaq/
  # cp -auv phypidaq/doc    $DIR/phypidaq/

  #copy config examples
  cp -auv config/ $DIR
  cp -auv *.daq $DIR

  # copy examples
  cp -auv examples/ $DIR
fi

echo -e "\nThe full documentation (software, hardware and educational guidelines) can be found on GitHub:"
echo -e "https://github.com/PhyPiDAQ"
