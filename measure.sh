#!/bin/bash

# Script for automated collection, conversion and analysis of waveforms via the mic input
# Remember that the mic gain can be found and adjusted using alsamixer (front mic boost)

# Usage: ./measure.sh MeasureTime GasTime WireID
# MeasureTime is the time in seconds to record the waveform for (must be an integer)
# GasTime is the time in ms to open the gas valve for (~20 is good)
# WireID is a string added to the filename (e.g. F4W01)

# To excite the string first activate gas jet
# This is achieved by sending an integer value over the serial port to the arduino
# This value is the lentgh in ms of the gas pulse (value should be in the range 10-25 ms)

# Uncomment the 2 exec commands if the serial port is not opened through another method (e.g. using the serial monitor of the arduino IDE)
# After updating to the latest version of Arduino software it seems using the serial monitor blocks communication

exec 3<> /dev/ttyACM1 && sleep 1.5
sleep 0.1
echo $2 > /dev/ttyACM1
sleep 0.05
exec 3>&-

# To specify the hardware channel (see output of 'arecord -l') 
#arecord -f dat -r 192000 -c 1 -d 1 -D plughw:0,0 waveform.wav
# Otherwise use the default selection
arecord -f dat -r 192000 -c 1 -d $1 waveform$4.wav

# Convert the binary wav to ascii format
sox waveform$4.wav waveform$4.dat

# Run analysis code on the saved waveform
python FFT.py waveform$4.dat waveform$4.txt $3
