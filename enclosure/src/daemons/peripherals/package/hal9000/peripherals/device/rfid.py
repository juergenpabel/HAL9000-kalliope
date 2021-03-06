#!/usr/bin/python3

import sys
import logging
from configparser import ConfigParser

from hal9000.peripherals.device import HAL9000_Device
from hal9000.peripherals.driver import HAL9000_Driver


class Device(HAL9000_Device):

	def __init__(self, name: str, Driver: HAL9000_Driver) -> None:
		HAL9000_Device.__init__(self, 'rfid:{}'.format(name), Driver)
		self.config = dict()
		self.driver = None
		self.logger = logging.getLogger()
		self.current_uid = None
 

	def configure(self, configuration: ConfigParser, section_name: str = None) -> None:
		HAL9000_Device.configure(self, configuration)
		peripheral, device = str(self).split(':')
		self.config['enabled'] = configuration.getboolean(str(self), 'rfid-enabled', fallback=True)
		if self.config['enabled']:
			self.driver = self.Driver('{}:{}'.format(configuration.getstring(str(self), 'driver'), device))
			self.driver.configure(configuration)
			if self.driver.getReaderVersion() is None:
				self.driver = None


	def do_loop(self, callback_event = None) -> bool:
		result = False
		if self.driver is not None:
			if self.driver.do_loop():
				result = True
				previous_uid = self.current_uid
				current_uid = self.driver.status['uid']
				if previous_uid != current_uid:
					self.current_uid = current_uid
					if callback_event is not None:
						peripheral, device = str(self).split(':',1)
						component, dummy = str(self.driver).split(':',1)
						if previous_uid is not None:
							self.logger.debug('device:{} => tag with uid "{}" absent'.format(self, previous_uid))
							callback_event(peripheral, device, component, 'leave', previous_uid)
						if current_uid is not None:
							self.logger.debug('device:{} => tag with uid "{}" detected'.format(self, current_uid))
							callback_event(peripheral, device, component, 'enter', current_uid)
 
		return result

