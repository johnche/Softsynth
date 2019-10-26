from synth import Synthesizer
import select, socket


class SynthController:
	def __init__(self, port):
		self.address = ("0.0.0.0", 5050)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.sock.bind(self.address)
		self.sock.listen(1)
		print('TCP server listening to %s %s' % self.address)
		print('Setting up synth')
		self.synth = Synthesizer()

	def run(self):
		print('Ready')
		self.conn, self.addr = self.sock.accept()
		print('TCP connection established', self.addr)

		while True:
			data = self.conn.recv(1024)
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

	def close(self):
		self.conn.close()
		self.sock.close()
		self.synth.close()


def main():
	control = SynthController(5050)
	control.run()


if __name__ == "__main__":
	main()

