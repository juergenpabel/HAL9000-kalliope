#!/usr/bin/python3

from hal9000.daemon import HAL9000_Daemon as HAL9000
from device import Device as Buttons


class Daemon(HAL9000):

	def __init__(self):
		HAL9000.__init__(self, 'buttons')
		self.buttons = Buttons()


	def configure(self, filename: str) -> None:
		HAL9000.configure(self, filename)
		self.buttons.configure()


	def do_loop(self) -> bool:
		self.buttons.do_loop()
		return True


if __name__ == "__main__":
	daemon = Daemon()
	daemon.configure(None)
	daemon.loop()

