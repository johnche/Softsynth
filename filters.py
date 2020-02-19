import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz


class Filter:
	def __init__(self, name, order=5):
		self.name = name
		self.module_name = 'Filter'
		self.order = order

	def plot_frequency_response(self, xlim=None):
		'''
		Only for debugging
		'''
		if not xlim:
			xlim = self.nyquist_frequency
		w, h = freqz(filt.b, filt.a, worN=8000)
		plt.plot(self.nyquist_frequency*w/np.pi, np.abs(h), 'b')

		plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
		plt.axvline(cutoff, color='k')

		plt.xlim(0, xlim)
		plt.grid()
		plt.show()


class LowpassFilter(Filter):
	def get_coefficients(self, cutoff, sampling_rate):
		'''
		Calculate new coefficients
		'''
		nyquist_frequency = 0.5 * sampling_rate
		normalized_cutoff = cutoff / nyquist_frequency
		return butter(self.order, normalized_cutoff, btype='low', analog=False)

	def __call__(self, data):
		params = data.get(self.name, None)
		if params:
			if not hasattr(self, 'cutoff') or self.cutoff != params['fc']:
				self.cutoff = params['fc']
				params['b'], params['a'] = self.get_coefficients(self.cutoff, data['fs'])
			data['samples'] = lfilter(params['b'], params['a'], data['samples'])
			data[self.name] = params
		return data

