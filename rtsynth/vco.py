import numpy as np


class Oscillator:
	def _create_samples(self, wave_array, frequency):
		return np.array_split(wave_array.astype(np.float32), frequency)


class SineOscillator(Oscillator):
	def __init__(self, sampling_rate):
		self.sampling_rate = sampling_rate
		self.samples = [np.zeros(500)]
		self.has_new_samples = False

	def update_parameters(self, frequency):
		n = np.arange(self.sampling_rate)
		t = n/self.sampling_rate
		omega = 2*np.pi*frequency
		wave = np.sin(omega*t)

		self.samples = self._create_samples(wave, frequency)
		self.has_new_samples = True

	def get_wave(self):
		while True:
			buffered_samples = self.samples
			for cycle in self.samples:
				if self.has_new_samples:
					self.has_new_samples = False
					break
				yield cycle.tobytes()

