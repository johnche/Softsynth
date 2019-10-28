from vco import SineOscillator
import pyaudio
import numpy as np

from time import sleep

class Synthesizer:
	def __init__(self):
		self.sampling_rate = 44100
		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(format=pyaudio.paFloat32,
				channels=1,
				rate=self.sampling_rate,
				output=True)
		
		self.vco = SineOscillator(self.sampling_rate)
		self.sample_generator = self.vco.get_wave()

		self.frequency = 442

	def set_frequency(self, frequency):
		self.frequency = frequency
		self.vco.update_parameters(frequency)

	def generate_samples(self, frequency):
		num_samples = np.floor(self.sampling_rate/frequency)
		n = np.linspace(0, 6*np.pi, 3*num_samples)
		wave = np.sin(n)
		wave = np.tile(wave, 2*frequency)
		self.samples = self._create_samples(wave)

	def _create_samples(self, wave_array):
		return wave_array.astype(np.float32).tobytes()

	def play(self):
		for cycle in self.sample_generator:
			self.stream.write(cycle)

	def close(self):
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()

