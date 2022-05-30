#!/usr/bin/python3

import re
from paho.mqtt.publish import single as mqtt_publish_message
from hal9000.abstract.plugin import HAL9000_Trigger as HAL9000
from configparser import ConfigParser


class Trigger(HAL9000):

	def __init__(self, trigger_name: str) -> None:
		HAL9000.__init__(self, 'mqtt', trigger_name)
		self.config = dict()


	def configure(self, configuration: ConfigParser, section_name: str) -> None:
		self.config['topic'] = configuration.getstring(section_name, 'mqtt-topic', fallback=None)
		self.config['payload-regex'] = configuration.getstring(section_name, 'mqtt-payload-regex', fallback=None)


	def callbacks(self) -> dict:
		result = dict()
		topics = list()
		if self.config['topic'] is not None:
			topics.append(self.config['topic'])
		result['mqtt'] = topics
		return result


	def handle(self, message) -> dict:
		matches = re.match(self.config['payload-regex'], message.payload.decode('utf-8'))
		if matches is not None:
			return matches.groupdict()
		return None

