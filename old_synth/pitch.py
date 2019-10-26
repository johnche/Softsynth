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
	notes['cs'] = 41
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

def refFrequency():
	return int(raw_input("A4 Reference frequency: "))

#TODO: Put in context of main
