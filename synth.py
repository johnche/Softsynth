import pyaudio
import numpy as np
from threading import Thread, Event
from pitches import MTS_PITCHES


class SoundDriver:
	def __init__(self, sampling_rate=44100):
		self.sampling_rate = sampling_rate
		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(format=pyaudio.paFloat32,
				channels=1,
				rate=self.sampling_rate,
				output=True)

	def push(self, samples):
		self.stream.write(samples)

	def close(self):
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()
		print('closed')


class ControlInterface(Thread):
	def __init__(self):
		Thread.__init__(self)

	def play(self, midi_num):
		self.midi_num = midi_num

	def stop(self):
		self.midi_num = -1

	def run(self):
		self.midi_num = -1
		while True:
			self.push(self.cache[self.midi_num])


class Synthesizer(SoundDriver, ControlInterface):
	def __init__(self, sampling_rate=44100):
		ControlInterface.__init__(self)
		SoundDriver.__init__(self, sampling_rate)
		self.cache = {-1: np.zeros(100).astype(np.float32).tobytes()}
		self.pipeline = []
		self.sampling_rate = sampling_rate
		self.settings = {'fs': sampling_rate}

	def __iadd__(self, module):
		self.pipeline.append(module)
		return self

	def add_metadata(self, midi_num):
		return {'f': MTS_PITCHES[midi_num], **self.settings}

	def set_lowpass(self, cutoff):
		self.settings['lpc'] = cutoff

	def update(self):
		print('Generating pitches..')
		for midi_num, frequency in MTS_PITCHES.items():
			data = self.add_metadata(midi_num)
			for pipe_step in self.pipeline:
				data = pipe_step(data)
			self.cache[midi_num] = data['data'].astype(np.float32).tobytes()
		print('Done.')

