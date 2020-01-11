import json
import numpy as np


def MTS(midi_number):
	'''
	MTS - MIDI Tuning Standard
	'''
	concert_A = 440
	exponent = (midi_number-69)/12
	return np.power(2, exponent)*concert_A


MTS_PITCHES = {midi_num: MTS(midi_num) for midi_num in range(0, 128)}
TABLE_PITCHES = json.load(open('misc/pitches.json', 'r'))
