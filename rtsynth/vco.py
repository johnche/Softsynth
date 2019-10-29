import numpy as np
from scipy import signal


class Oscillator:
	def __init__(self, sampling_rate):
		self.sampling_rate = sampling_rate
		self.samples = np.zeros(500)
		self.has_new_samples = False

	def get_samplesPerCycle(self, frequency):
		return int(self.sampling_rate/frequency)

	def _create_silence(self):
		return np.zeros(100)

	def get_wave(self):
		while True:
			yield self.samples


class SineOscillator(Oscillator):
	def update_parameters(self, frequency):
		print('Frequency', frequency)
		if frequency == 0:
			self.samples = self._create_silence()
		else:
			samplesPerCycle = self.get_samplesPerCycle(frequency)

			# ALT 1, litt raspete
			#x = np.linspace(0, 2*np.pi, samplesPerCycle)
			#self.samples = np.sin(x).astype(np.float32).tobytes()

			# ALT 2, har artifakter i frekvensskifte
			n = np.arange(samplesPerCycle)
			t = n/self.sampling_rate
			omega = 2*np.pi*frequency
			wave = np.sin(omega*t)
			self.samples = wave.astype(np.float32).tobytes()


class SquareOscillator(Oscillator):
	def update_parameters(self, frequency):
		if frequency == 0:
			self.samples = self._create_silence()
		else:
			samplesPerCycle = self.get_samplesPerCycle(frequency)
			t = np.linspace(0, 2*np.pi, samplesPerCycle)
			self.samples = signal.square(t).astype(np.float32).tobytes()


class SawtoothOscillator(Oscillator):
	def update_parameters(self, frequency):
		if frequency == 0:
			self. samples = self._create_silence()
		else:
			samplesPerCycle = self.get_samplesPerCycle(frequency)
			self.samples = np.linspace(1, -1, samplesPerCycle)


class TriangleOscillator(Oscillator):
	# Skremmer livet av folk
	def update_parameters(self, frequency):
		if frequency == 0:
			self. samples = self._create_silence()
		else:
			samplesPerCycle = self.get_samplesPerCycle(frequency)
			t = np.linspace(0, 2*np.pi, samplesPerCycle)
			self.samples = signal.sawtooth(t, width=0.5)
			print(self.samples)

