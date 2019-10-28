import numpy as np


class Oscillator:
	def __init__(self, sampling_rate):
		self.sampling_rate = sampling_rate
		self.samples = np.zeros(500)
		self.has_new_samples = False

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
			n = np.arange(int(self.sampling_rate/frequency))
			t = n/self.sampling_rate
			omega = 2*np.pi*frequency
			wave = np.sin(omega*t)
			self.samples = wave.astype(np.float32).tobytes()

