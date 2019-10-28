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
		if key == keyboard.Key.up:
			self.synth.set_frequency(self.synth.frequency + 1)
		elif key == keyboard.Key.down:
			self.synth.set_frequency(self.synth.frequency - 1)
	
	def on_release(self, key):
		if key == keyboard.Key.esc:
			return False

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

