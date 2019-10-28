from synth import Synthesizer
from pynput import keyboard
import select, socket


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

	def on_press(self, key):
		try:
			if key.char == 'a':
				self.synth.set_frequency(262)
			elif key.char == 's':
				self.synth.set_frequency(294)
			elif key.char == 'd':
				self.synth.set_frequency(330)
			elif key.char == 'f':
				self.synth.set_frequency(349)
			elif key.char == 'g':
				self.synth.set_frequency(392)
			elif key.char == 'h':
				self.synth.set_frequency(440)
			elif key.char == 'j':
				self.synth.set_frequency(494)
			elif key.char == 'k':
				self.synth.set_frequency(523)

			elif key.char == 'w':
				self.synth.set_frequency(278)
			elif key.char == 'e':
				self.synth.set_frequency(311)
			elif key.char == 't':
				self.synth.set_frequency(370)
			elif key.char == 'y':
				self.synth.set_frequency(415)
			elif key.char == 'u':
				self.synth.set_frequency(466)
		except AttributeError:
			if key == keyboard.Key.up:
				self.synth.set_frequency(self.synth.frequency + 1)
			elif key == keyboard.Key.down:
				self.synth.set_frequency(self.synth.frequency - 1)
	
	def on_release(self, key):
		if key == keyboard.Key.esc:
			return False
		else:
			self.synth.set_frequency(0)

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

