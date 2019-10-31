from synth import Synthesizer
from pynput import keyboard
import select, socket, json


class SynthController:
	def __init__(self, port):
		#self.address = ("0.0.0.0", port)
		#self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		#self.sock.bind(self.address)
		#self.sock.listen(1)
		#print('TCP server listening to %s %s' % self.address)
		print('Setting up synth')
		self.synth = Synthesizer()
		with open('pitches.json', 'r') as f:
			self.lookup_json = json.load(f)
		self.pitches = [self.lookup_json[octave] for octave in self.lookup_json]

		self.current_octave = 4
		self.pressed_keys = []

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
			pitch_name = ''
			if key.char == 'a': pitch_name = 'C'
			elif key.char == 'w': pitch_name = 'C#'
			elif key.char == 's': pitch_name = 'D'
			elif key.char == 'e': pitch_name = 'D#'
			elif key.char == 'd': pitch_name = 'E'
			elif key.char == 'f': pitch_name = 'F'
			elif key.char == 't': pitch_name = 'F#'
			elif key.char == 'g': pitch_name = 'G'
			elif key.char == 'y': pitch_name = 'G#'
			elif key.char == 'h': pitch_name = 'A'
			elif key.char == 'u': pitch_name = 'A#'
			elif key.char == 'j': pitch_name = 'B'
			elif key.char == 'k':
				self.synth.set_frequency(self.pitches[self.current_octave+1]['C'])

			if pitch_name:
				self.synth.set_frequency(self.pitches[self.current_octave][pitch_name])

			self.register_key(key.char)
		except AttributeError:
			if key == keyboard.Key.up:
				if self.current_octave < 8:
					self.current_octave += 1
			elif key == keyboard.Key.down:
				if self.current_octave > 0:
					self.current_octave -= 1

			elif key == keyboard.Key.left:
				if self.synth.oscillator_index > 0:
					self.synth.set_oscillator(self.synth.oscillator_index - 1)
			elif key == keyboard.Key.right:
				if self.synth.oscillator_index < 3:
					self.synth.set_oscillator(self.synth.oscillator_index + 1)

			print('Current octave', self.current_octave)
			print('Current oscillator index', self.synth.oscillator_index)
	
	def on_release(self, key):
		if key == keyboard.Key.esc:
			self.close()
			return False
		else:
			try:
				self.pressed_keys.remove(key.char)
				if not self.pressed_keys:
					self.synth.set_frequency(0)
			except AttributeError:
				pass

	def run_keyboard(self):
		listener = keyboard.Listener(
				on_press=self.on_press,
				on_release=self.on_release)
		listener.start()

		self.synth.play()

	def close(self):
		self.conn.close()
		self.sock.close()
		self.synth.close()


def main():
	control = SynthController(5050)
	control.run_keyboard()
	#control.run_socket()


if __name__ == "__main__":
	main()

