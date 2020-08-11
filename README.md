# TensionMeasurement
Measurement of MWPC wire tensions using a laser system.

An Arduino Uno is used to control a solenoid valve to provide a burst of air directed at the wire to be measured shortly before the diode response is recorded. A motor shield is used to drive the solenoid and the Adafruit motor shield library V2 used for control.

The diode response is passed through a preamplifier and digitised using the desktop soundcard (connected through the front mic in line). The a fast fourier transform is performed on the recorded waveform using python to extract the fundamental frequency, hence tension, of the wire.
