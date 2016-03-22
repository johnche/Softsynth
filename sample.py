######################################
#                                    #
#                                    #
#        Sample Calculation          #
#                                    #
#                                    #
######################################


def superPosition(wave1, wave2):
	longwave1 = map(long, wave1)
	longwave2 = map(long, wave2)
	dataList = map(add, longwave1, longwave2)
	if (max(dataList) <= 32767):
		return dataList
	else:
		normList = [x*(32767/max(dataList)) for x in dataList]
		return normList

#TODO: filter

def zipper(waves):
	#Binarysuperpositioning
	n = len(waves)
	if (n > 2): 
		wave = [zipper(waves[:(n/2)])]
		wave2 = [zipper(waves[(n/2):])]
	if (n == 1): return waves
	return superposition(wave, wave2)
#>--#does this work?



def timbre():
	#TODO: Instrument library
	pass

def harmonics(wave):
	pass

