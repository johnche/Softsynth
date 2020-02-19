import pyaudio
import numpy as np
from threading import Thread, Event
from collections import defaultdict
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
		'''
		@samples: float32 bytes / .astype(np.float32).tobytes()
		'''
		self.stream.write(samples)

	def close(self):
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()
		print('closed')


class SynthUI(SoundDriver, Thread):
	def __init__(self, sampling_rate):
		Thread.__init__(self)
		SoundDriver.__init__(self, sampling_rate)
		self.settings = {'fs': sampling_rate}

	def play(self, midi_num):
		self.midi_num = midi_num

	def stop(self):
		self.midi_num = -1

	def update_parameter(self, name, entry):
		if type(entry) == dict:
			self.settings[name] = {**self.settings[name], **entry}
		else:
			self.settings[name] = entry

	def update_parameters(self, params):
		self.settings = {**self.settings, **params}

	def run(self):
		self.midi_num = -1
		while True:
			self.push(self.cache[self.midi_num])


class Wave:
	def __init__(self, samples, chunk_size=100):
		self.attack = []
		self.release = []
		self.stop = False
		self.sustain = samples['sustain']
		if type(samples) == dict:
			self.attack = self.split(samples['attack'], chunk_size)
			self.release = self.split(samples['release'], chunk_size)

	def split(self, samples, chunk_size):
		if samples.size >= chunk_size:
			num_rest_samples = samples.size % chunk_size
			first_chunk = samples[:num_rest_samples]
			full_chunks = np.split(samples[num_rest_samples:], samples.size//chunk_size)
			samples = np.concatenate(first_chunk, full_chunks)
		return samples

	def _generate(self, chunks):
		for chunk in chunks:
			yield chunk

	def stop(self):
		self.stop = True

	def get_samples(self):
		for chunk in self.attack:
			if self.stop:
				break
			yield chunk

		while not self.stop:
			yield self.sustain

		for chunk in self.release:
			yield chunk

	def end(self):
		self.stop = True


class SynthChannel:
	def __init__(self, oscillator):
		self.source = oscillator
		self.pipeline = []

	def __iadd__(self, module):
		self.pipeline.append(module)
		return self

	def __str__(self):
		return 


class Synthesizer(SynthUI):
	# TODO: default parameters
	def __init__(self, sampling_rate=44100):
		SynthUI.__init__(self, sampling_rate)
		self.cache = {-1: np.zeros(100).astype(np.float32).tobytes()}
		self.pipeline = []

	def __iadd__(self, module):
		self.pipeline.append(module)
		return self

	def add_metadata(self, midi_num):
		return {'f': MTS_PITCHES[midi_num], **self.settings}

	def add_channel(self, synth_channel):
		self.channels.append(synth_channel)

	def update(self):
		print('Generating pitches..')
		for midi_num, frequency in MTS_PITCHES.items():
			data = self.add_metadata(midi_num)
			for pipe_step in self.pipeline:
				data = pipe_step(data)

			self.cache[midi_num] = data['samples'].astype(np.float32).tobytes()
		print('Done.')

