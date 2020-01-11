import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz


class Filter:
	def __init__(self, sample_rate=44100, order=5):
		self.nyquist_frequency = 0.5*sample_rate
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
	def _update(self, cutoff):
		'''
		Calculate new coefficients
		'''
		normalized_cutoff = cutoff / self.nyquist_frequency
		self.b, self.a = butter(self.order, normalized_cutoff, btype='low', analog=False)

	def __call__(self, data):
		if not hasattr(self, 'cutoff') or self.cutoff != data['lpc']:
			self.cutoff = data['lpc']
			self._update(self.cutoff)
		data['data'] = lfilter(self.b, self.a, data['data'])
		return data

