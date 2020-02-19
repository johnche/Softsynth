import numpy as np


def normalize(data):
	if data.max() > 1:
		pass
	elif data.min() < -1:
		pass


class Amplifier:
	def __init__(self, name):
		self.name = name

	def __call__(data):
		amp_type = type(data['amp'])
		if amp_type == float:
			pass
		elif amp_type == dict:
			pass
		else:
			amp = 1
		envelope = self.adsr(data)
		data = self.apply(envelope, data)
		amp = data.get('amp', 1)
		data['data'] = amp*normalize(data['data'])
		return data

	def adsr(data):
		'''
		ADSR params are given in ms units
		'''
		params = data['adsr']
		sample_length = 1000/data['fs']
		num_attack_samples = int(params['Attack']/sample_length)
		num_decay_samples = int(params['Decay']/sample_length)
		num_attack_samples = int(params['Release']/sample_length)
	
		attack_samples = np.linspace(0, 1, num_attack_samples, endpoint=False)
		decay_samples = np.linspace(1, params['Sustain'], num_decay_samples, endpoint=False)
		release_samples = np.linspace(params['Sustain'], 0)
	
		envelope = {
				'begin': np.concatenate((attack_samples, decay_samples)),
				'end': release_samples
				}
		data['adsr'] = envelope
		return data['adsr']
	
