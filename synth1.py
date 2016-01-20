import math, wave, array
import matplotlib.pyplot as plt #graphtesting
import numpy as np #listgenerator
import os, sys #os.remove
import random

#TODO: Pitches, superposition
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


######################################
#                                    #
#                                    #
#        Sample Calculation          #
#                                    #
#                                    #
######################################


def sine(x):
	return math.sin(2 * math.pi * x)

def sinew(amplitude, samplesPerCycle, i):
	return int(amplitude * sine((i % samplesPerCycle)/float(samplesPerCycle))) #Denominator must be float, python casts the whole fraction to int because tilbakestaaende.

def saw(amplitude, samplesPerCycle, i):
	return int(amplitude * (i % samplesPerCycle)/samplesPerCycle)

def triangle(amplitude, samplesPerCycle, i):
	if (i % (samplesPerCycle * 2) < samplesPerCycle):
		sample = amplitude * (i % samplesPerCycle)/samplesPerCycle
	else:
		sample = amplitude * (samplesPerCycle - (i % samplesPerCycle))/samplesPerCycle
	return int(sample)

def square(amplitude, samplesPerCycle, i):
	#TODO: Modifiable frequency
	if (i % (samplesPerCycle * 2) < samplesPerCycle):
		sample = amplitude
	else:
		sample = amplitude/2
	return int(sample)

######################################
#                                    #
#                                    #
#          Pitch calculation         #
#                                    #
#                                    #
######################################

def setNotes():
	notes = {}
	notes['c'] = 40
	notes['d'] = 42
	notes['e'] = 44
	notes['f'] = 45
	notes['g'] = 47
	notes['a'] = 49
	notes['h'] = 51
	notes['c2'] = 52
	return notes

def makePitch(origin, note, sampleRate, duration, amplitude, samplesPerCycle, wavefunc):
	numSamples = sampleRate * duration
	frequency = pitchFrequencies(origin, note)
	return calculateSamples(numSamples, amplitude, samplesPerCycle, wavefunc)

def pitchFrequencies(origin, note):
	return math.pow(2,((note-49)/12.0))*origin

def inputTune():
	return raw_input("Input pitch or x to end: ")

def generateTune(notes):
	#Static duration
	tune = []
	while True:
		print tune
		tone = inputTune()
		if (tone not in notes.keys() and not tone  == 'x'):
			print "Not a valid pitch"
		elif (tone == 'x'):
			return tune
		else:
			tune.append(tone)
		print "something"

def createTune(sampleRate, amplitude, notes, wavefunc):
	#Use generateTune and makePitch to create series of pitches
	#TODO: split the function
	tune = []
	data = array.array('h')
	dataList = []
	duration = 1
	numSamples = sampleRate * duration
	sumDuration = 0
	sumSamples = 0
	#TODO: Add different duration per pitch functionality
	#TODO: Make each unique duration metronome dependent
	refFrequency = int(raw_input("A4 Reference frequency: "))
	print notes
	while True:
		if (len(tune) < 1):
			tune = generateTune(notes)
		else: break
	for i in tune:
		frequency = pitchFrequencies(refFrequency, notes[i])
		print "frequency ", notes[i], frequency
		samplesPerCycle = int(sampleRate / frequency)
		numSamples = duration * sampleRate
		sumDuration += 1 #TODO: change this when duration per pitch != 1 second
		for j in range(numSamples):
			sample = wavefunc(amplitude, samplesPerCycle, j)
			data.append(sample)
			dataList.append(sample)
	sumSamples = sumDuration * sampleRate
	print dataList
	return dataList, data, sumSamples

if __name__=="__main__":
	# Initialization of data, structure for storing intensities
	data = array.array('h')
	# Initialization of wavefileheader
	volume = 100
	channels = 1 #mono/stereo
	dataSize = 2
	sampleRate = 44100 #samples per sec
	amplitude = 32767 * float(volume) / 100
	notes = setNotes()
	dataList, data, sumSamples = createTune(sampleRate, amplitude, notes, sinew)

	#WRITE TO FILE
	#os.remove("Sinus.wav")
	saveToFile(channels, dataSize, sampleRate, sumSamples)

	#TESTING
	graphData(sampleRate, dataList)
