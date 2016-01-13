import math, wave, array

duration = 1
frequency = 440
volume = 100
amplitude = 32767 * float(volume) / 100
data = array.array('h')
sampleRate = 44100
channels = 1
dataSize = 2
numSamples = sampleRate * duration
samplesPerCycle = int(sampleRate / frequency)
#deltaFrequency = 0

for i in range(numSamples):
	sample = amplitude * math.sin(math.pi * 2 * (i % samplesPerCycle)/samplesPerCycle)
	data.append(int(sample))
	#deltaFrequency += 1;
save = wave.open('Sinus440Hz.wav','w')
save.setparams((channels, dataSize, sampleRate, numSamples, "NONE", "Uncompressed"))
save.writeframes(data.tostring())
save.close()
