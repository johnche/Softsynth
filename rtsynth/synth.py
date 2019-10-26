import pyaudio
import numpy as np


class Synthesizer:
	def __init__(self):
		self.sampling_rate = 44100
		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(format=pyaudio.paFloat32,
				channels=1,
				rate=self.sampling_rate,
				output=True)

	def set_frequency(self, frequency):
		stuff = frequency/self.sampling_rate
		wave = np.sin(2*np.pi*np.arange(self.sampling_rate)*stuff)
		self.samples = self._create_samples(wave)

	def _create_samples(self, wave_array):
		return wave_array.astype(np.float32).tobytes()

	def play(self):
		if self.samples:
			self.stream.write(self.samples)

	def close(self):
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()

