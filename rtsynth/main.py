import select, socket
from synth import Synthesizer
from pynput import keyboard
from pitches import TABLE_PITCHES 
from oscillators import SineOscillator
from filters import LowpassFilter


class SynthController:
	def __init__(self, port, synthesizer):
		#self.address = ("0.0.0.0", port)
		#self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		#self.sock.bind(self.address)
		#self.sock.listen(1)
		#print('TCP server listening to %s %s' % self.address)
		print('Setting up synth')
		self.synth = synthesizer
		self.lookup_json = TABLE_PITCHES
		self.pitches = [self.lookup_json[octave] for octave in self.lookup_json]

		self.current_octave = 4
		self.pressed_keys = []
		self.midi_num = 50
		self.lp_c = 1000
		self.lp = LowpassFilter()

		self.synth += SineOscillator
		self.synth += self.lp
		self.synth.set_lowpass(self.lp_c)
		self.synth.update()
		self.synth.start()

	def run_socket(self):
		print('Ready')
		self.conn, self.addr = self.sock.accept()
		print('TCP connection established', self.addr)

		while True:
			data = self.conn.recv(8)
			if not data:
				break

			try:
				frequency = int(data)
				print('New frequency', frequency)
				self.synth.set_frequency(frequency)
				self.synth.play()
			except ValueError as e:
				print('Unacceptable value', data)
				break

		print('Exiting.')
		self.close()

	def register_key(self, key):
		if key not in self.pressed_keys:
			self.pressed_keys.append(key)

	def on_press(self, key):
		try:
			#pitch_name = ''
			#if key.char == 'a': pitch_name = 'C'
			#elif key.char == 'w': pitch_name = 'C#'
			#elif key.char == 's': pitch_name = 'D'
			#elif key.char == 'e': pitch_name = 'D#'
			#elif key.char == 'd': pitch_name = 'E'
			#elif key.char == 'f': pitch_name = 'F'
			#elif key.char == 't': pitch_name = 'F#'
			#elif key.char == 'g': pitch_name = 'G'
			#elif key.char == 'y': pitch_name = 'G#'
			#elif key.char == 'h': pitch_name = 'A'
			#elif key.char == 'u': pitch_name = 'A#'
			#elif key.char == 'j': pitch_name = 'B'
			#elif key.char == 'k':
			#	self.synth.set_frequency(self.pitches[self.current_octave+1]['C'])

			#if pitch_name:
			#	self.synth.set_frequency(self.pitches[self.current_octave][pitch_name])

			if key.char == 'a':
				self.synth.play(self.midi_num)

			self.register_key(key.char)
		except AttributeError:
			if key == keyboard.Key.up:
				if self.midi_num < 128:
					self.midi_num += 1
					self.synth.play(self.midi_num)
					print('Midi number', self.midi_num)
			elif key == keyboard.Key.down:
				if self.midi_num >= 0:
					self.midi_num -= 1
					self.synth.play(self.midi_num)
					print('Midi number', self.midi_num)
			elif key == keyboard.Key.left:
				self.lp_c -= 1
				print('Lowpass cutoff', self.lp_c)
				self.synth.set_lowpass(self.lp_c)
				self.synth.update()
			elif key == keyboard.Key.right:
				self.lp_c += 1
				print('Lowpass cutoff', self.lp_c)
				self.synth.set_lowpass(self.lp_c)
				self.synth.update()

			#if key == keyboard.Key.up:
			#	if self.current_octave < 8:
			#		self.current_octave += 1
			#elif key == keyboard.Key.down:
			#	if self.current_octave > 0:
			#		self.current_octave -= 1

			#elif key == keyboard.Key.left:
			#	if self.synth.oscillator_index > 0:
			#		self.synth.set_oscillator(self.synth.oscillator_index - 1)
			#elif key == keyboard.Key.right:
			#	if self.synth.oscillator_index < 3:
			#		self.synth.set_oscillator(self.synth.oscillator_index + 1)

			#print('Current octave', self.current_octave)
			#print('Current oscillator index', self.synth.oscillator_index)
	
	def on_release(self, key):
		if key == keyboard.Key.esc:
			pass
			#self.close()
			#return False
		else:
			try:
				self.pressed_keys.remove(key.char)
				if not self.pressed_keys:
					self.synth.stop()
			except AttributeError:
				pass

	def run_keyboard(self):
		listener = keyboard.Listener(
				on_press=self.on_press,
				on_release=self.on_release)
		listener.start()

	def close(self):
		#self.conn.close()
		#self.sock.close()
		#self.synth.close()
		from sys import exit
		exit()


def main():
	synth = Synthesizer()

	control = SynthController(5050, synth)
	control.run_keyboard()
	#control.run_socket()


if __name__ == "__main__":
	main()

