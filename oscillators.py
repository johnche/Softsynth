import numpy as np
from scipy import signal


def SineOscillator(data):
	samplesPerCycle = int(data['fs']/data['f'])
	n = np.arange(samplesPerCycle)
	t = n/data['fs']
	omega = 2*np.pi*data['f']
	data['samples'] = np.sin(omega*t)
	return data


def SquareOscillator(data):
	samplesPerCycle = int(data['fs']/data['f'])
	t = np.linspace(0, 2*np.pi, samplesPerCycle)
	return signal.square(t)


def SawOscillator(data):
	samplesPerCycle = int(data['fs']/data['f'])
	return np.linspace(1, -1, samplesPerCycle)


def TriangleOscillator(data):
	samplesPerCycle = int(data['fs']/data['f'])
	t = np.linspace(0, 2*np.pi, samplesPerCycle)
	return signal.sawtooth(t, width=0.5)

