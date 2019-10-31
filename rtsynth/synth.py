from vco import SineOscillator, SquareOscillator, SawtoothOscillator, TriangleOscillator
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

		self.oscillators = [
				SineOscillator(self.sampling_rate),
				SquareOscillator(self.sampling_rate),
				SawtoothOscillator(self.sampling_rate),
				TriangleOscillator(self.sampling_rate)
				]
		self.oscillator_index = 0
		self.vco = self.oscillators[0]
		self.sample_generator = self.vco.get_wave()

	def set_oscillator(self, index):
		self.oscillator_index = index

		# Switcherooo
		self.vco.active = False
		self.vco = self.oscillators[index]
		self.sample_generator = self.vco.get_wave()
		self.vco.active = True

	def set_frequency(self, frequency):
		self.frequency = frequency
		self.vco.update_parameters(frequency)

	def play(self):
		while True:
			for cycle in self.sample_generator:
				self.stream.write(cycle)

	def close(self):
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()

