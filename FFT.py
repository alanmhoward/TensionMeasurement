# Script for performing frequency analysis of captured waveforms

import sys # Access to passed arguments and exit command
import os # Used for checking file existence

import numpy as np
from numpy import fft # get fft method from numpy
import matplotlib.pyplot as plt # for plotting

#import scipy as sci
from scipy.optimize import curve_fit # For fitting
#from scipy.signal import blackman
#from scipy.signal import hanning


# Turn windowing on or off
Windowing = True

# Define a function for fitting - a Gaussian on a flat background
def fit_function(x, a, x0, sigma, bg):
    return bg + a*np.exp(-(x-x0)**2/(2*sigma**2))

# Check that we have a filename provided
if (len(sys.argv) != 4):
  print "Expected a datafile, output file and centroid estimate"
  sys.exit(1)

# Get the input file name and check that the file exists
InputFile = sys.argv[1]
# Set the output file name
OutputFile = sys.argv[2]

# Get the estimated centroid
centroid = float(sys.argv[3])

print "Opening input file: " + InputFile
  
if os.path.isfile(InputFile) is not True:
  print 'Error: ' + InputFile + ' does not exist'
  sys.exit(2)
  
# Open the file we wish to work with in read mode
infile = open(InputFile, 'r')
# arrays for holding the time (x) and amplitude (y) data
xarray = []
yarray = []

# Loop over the file and read in values
for line in infile:
  values = line.split()
  if (values[0] == ';'): # Skip header lines
    continue
  else:
    #print values[0] + ' ' + values[1]
    xarray.append(float(values[0]))
    yarray.append(float(values[1]))

infile.close()

# Get some information on the data - sampling time and rate
Entries = len(xarray)
print str(Entries) + " entries"
ti = xarray[0]; # First time entry
tf = xarray[-1]; # Last time entry

SampleTime = tf-ti
SampleRate = (Entries - 1.0)/SampleTime

print "Sampling time = " + str(round(SampleTime,2)) + " s"
print "Sampling rate = " + str(round(SampleRate)) + " Hz"

# Create a window and modify the signal
if (Windowing == True):
  window = np.hamming(Entries)
  yarray_window = yarray * window

# Perform the FFT (use rfft for real component)
Mag = fft.rfft(yarray_window)

# Get values for the frequency axis (again use rfftfreq for real values)
# Returns a list of frequencies for a number of samples with a given period between samples
f = fft.rfftfreq(Entries, 1/round(SampleRate))

RealFreq = np.absolute(Mag)

# Write the frequency data to disk
output = open(OutputFile,'w')
for i in range (0,len(f)):
	output.write(str(f[i]) + " " + str(RealFreq[i]) + "\n" )
output.close()



# Curve fitting
# Make a mask to cover only the region of interest (centroid plus/minus 60 Hz)
fmask = (f >= centroid-60) & (f <= centroid+60)
# Fit the function defined earlier over this region, providing some reasonable gues of initial parameters
popt, pcov = curve_fit(fit_function, f[fmask], RealFreq[fmask], p0 = [1,centroid,1,1])

print "Centroid at " + str(round(popt[1],2)) + u"\u00B1" + str(round(pcov[1,1]**0.5,2))

# Setup subplots
fig, ax = plt.subplots(4,1, figsize=(10,15))

# Plot a portion of the raw waveform
ax[0].set_title("Raw waveform")
ax[0].plot(xarray,yarray)
ax[0].set_xlabel("Time (s)")
ax[0].grid(True)

# Plot the windowed waveform
ax[1].set_title("Windowed waveform")
#ax[1].plot(xarray,yarray,marker='o') # Use this to show measurement points - can be problematic used with pdf output
ax[1].plot(xarray,yarray_window)
ax[1].set_xlabel("Time (s)")
ax[1].grid(True)

# Plot an overview of the transform
ax[2].set_title("Frequency response")
ax[2].plot(f, RealFreq, drawstyle='steps')
ax[2].set_xlabel("Frequency (Hz)")
ax[2].set_xlim(xmin=0, xmax=2000)
ax[2].set_yscale("log")
ax[2].grid(True)

# Zoom in on the interesting region of the transform
ax[3].set_title("Frequency response (zoomed)")
# The autoscale will scale over all x values - make a subplot using a mask to autoscale y only over the x range of interest
ax[3].plot(f[fmask], RealFreq[fmask], drawstyle='steps')
ax[3].plot(f[fmask], fit_function(f[fmask], popt[0], popt[1], popt[2], popt[3]), '-r')
ax[3].set_xlabel("Frequency (Hz)")
ax[3].grid(True)

plt.tight_layout() # avoid axis lables overlapping

# Either show the plot or write the plot to file
plt.show()
plt.savefig("waveform.png")

