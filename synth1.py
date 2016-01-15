import math, wave, array
import matplotlib.pyplot as plt #graphtesting
import numpy as np #listgenerator
import os, sys #os.remove
import random

def graphData(limit, samples):
	view = 500 #number of samples included
	domain = np.arange(1,view+1)
	print samples[0:view]
	plt.plot(domain, samples[0:view], 'bs') #plot(x,y, 'bluesquares')
	plt.ylabel('Sample')
	plt.xlabel('Time')
	plt.show()

def saveToFile(channels, dataSize, sampleRate, numSamples):
	save = wave.open('Sinus.wav','w')
	save.setparams((channels, dataSize, sampleRate, numSamples, "NONE", "Uncompressed"))
	save.writeframes(data.tostring())
	save.close()

def sine(x):
	print "x ", x
	return math.sin(2 * math.pi * x)

def sinew(amplitude, samplesPerCycle, i):
	print (i % samplesPerCycle)/samplesPerCycle
	return int(amplitude * sine((i % samplesPerCycle)/samplesPerCycle))


def square(amplitude, samplesPerCycle, i):
	#TODO: Modifiable frequency
	onoff = False
	for i in range(numSamples):
		if (i % samplesPerCycle == 0): onoff = not onoff
		if onoff: sample = amplitude
		if not onoff: sample = amplitude/2
		data.append(int(sample))
		dataList.append(int(sample))
	return data, dataList

def saw(amplitude, samplesPerCycle, i):
	print (i % samplesPerCycle)/samplesPerCycle
	return int(amplitude * (i % samplesPerCycle)/samplesPerCycle)

def calculateSamples(numSamples, amplitude, samplesPerCycle):
	dataList= []
	data = array.array('h')
	for i in range(numSamples):
		#data.append(square(amplitude, samplesPerCycle, i))
		#dataList.append(square(amplitude, samplesPerCycle, i))

		data.append(saw(amplitude, samplesPerCycle, i))
		dataList.append(saw(amplitude, samplesPerCycle, i))

		#data.append(sinew(amplitude, samplesPerCycle, i))
		#dataList.append(sinew(amplitude, samplesPerCycle, i))
	return dataList, data


if __name__=="__main__":
	# Initialization of data, structure for storing intensities
	data = array.array('h')
	# Initialization of wavefileheader
	volume = 100
	channels = 1 #mono/stereo
	dataSize = 2
	duration = 3
	sampleRate = 44100 #samples per sec
	frequency = int(raw_input("Frequency: "))
	print frequency
	amplitude = 32767 * float(volume) / 100
	numSamples = sampleRate * duration
	samplesPerCycle = int(sampleRate / frequency)
	print samplesPerCycle
	dataList, data = calculateSamples(numSamples, amplitude, samplesPerCycle)

	#WRITE TO FILE
	#os.remove("Sinus.wav")
	saveToFile(channels, dataSize, sampleRate, numSamples)

	#TESTING
	graphData(sampleRate, dataList)
