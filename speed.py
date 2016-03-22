######################################
#                                    #
#                                    #
#          Rythm calculation         #
#                                    #
#                                    #
######################################

def calculateBpm(bpm):
	return (bpm/60.0) #beats per second

def setBpm():
	while True:
		bpm = int(raw_input("Input BPM (standard is 120): "))
		if (bpm < 1): print "Error: BPM"
		else: return bpm
		#TODO: Exception handling for non-integer input

def getSpeed():
	return 1/calculateBpm(setBpm())

def duration(notelength, tempo):
	#Notelength exception handling?
	base = 4
	return (notelength * tempo)/float(base)

