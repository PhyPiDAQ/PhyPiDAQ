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

DIR=$HOME/$USERDIR
echo "copying files to "$DIR

mkdir -p $DIR

if [ -d $DIR ]; then
# enter here, if directory exists

  # create desktop icon
  cp -auv *.desktop $HOME/Desktop
  chmod a+x $HOME/Desktop/*.desktop

  # copy documentation
  # mkdir -p $DIR/doc
  # cp -auv doc/*.pdf $DIR/doc/
  # cp -auv README_de.pdf $DIR

  #copy python code
  cp -auv phypi.py $DIR
  cp -auv run_phypi.py $DIR
  cp -auv phypidaq/images/PhiPi_icon.png $DIR

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
