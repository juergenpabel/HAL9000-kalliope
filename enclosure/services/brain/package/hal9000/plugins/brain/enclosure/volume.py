#!/usr/bin/python3

import configparser
import json

from hal9000.brain.daemon import Daemon
from hal9000.plugins.brain.enclosure import EnclosureComponent


class Volume(EnclosureComponent):
	def __init__(self, **kwargs) -> None:
		EnclosureComponent.__init__(self, **kwargs)
		self.config = dict()


	def configure(self, configuration: configparser.ConfigParser, section_name: str, cortex: dict) -> None:
		EnclosureComponent.configure(self, configuration, section_name, cortex)
		if 'volume' not in cortex['enclosure']:
			cortex['enclosure']['volume'] = dict()
		self.config['volume-step']    = configuration.getint('enclosure:volume', 'volume-step',    fallback=5)
		self.config['initial-mute']   = configuration.getboolean('enclosure:volume', 'initial-mute', fallback=False)
		self.config['initial-volume'] = configuration.getint(    'enclosure:volume', 'initial-volume', fallback=50)


	def process(self, signal: dict, cortex: dict) -> None:
		EnclosureComponent.process(self, signal, cortex)
		if 'brain' in signal:
			if 'ready' in signal['brain']:
				cortex['enclosure']['volume']['level'] = self.config['initial-volume']
				if self.config['initial-mute'] is True:
					self.set_mute(cortex, self.config['initial-mute'])
				else:
					self.set_volume(cortex, self.config['initial-volume'])
			return
		if 'gui/overlay' in self.daemon.timeouts:
			timeout, overlay = self.daemon.timeouts['gui/overlay']
			if overlay != 'volume':
				self.daemon.video_gui_overlay_hide(overlay)
				del self.daemon.timeouts['gui/overlay']
		if cortex['#activity']['audio'].module == "none":
			if 'delta' in signal['volume']:
				if cortex['enclosure']['volume']['mute'] is False:
					delta = int(signal['volume']['delta']) * self.config['volume-step']
					volume = cortex['enclosure']['volume']['level'] + delta
					volume = min(volume, 100)
					volume = max(volume, 0)
					self.set_volume(cortex, volume)
					self.daemon.video_gui_overlay_show('volume', ({"level": str(cortex['enclosure']['volume']['level']), "mute": "false"}), 3)
			if 'mute' in signal['volume']:
				mute = not(cortex['enclosure']['volume']['mute'])
				self.set_mute(cortex, mute)
				self.daemon.video_gui_overlay_show('volume', ({"level": str(cortex['enclosure']['volume']['level']), "mute": str(mute).lower()}), 3)


	def set_mute(self, cortex: dict, mute: bool) -> None:
		cortex['enclosure']['volume']['mute'] = mute
		volume = int(cortex['enclosure']['volume']['level'])
		if mute is True:
			volume = 0
		self.daemon.queue_signal('mqtt', {'mqtt': {'topic': 'hal9000/command/kalliope/volume', 'payload': {'level': volume}}})
		self.daemon.logger.info('AUDIO: mute={}'.format(str(cortex['enclosure']['volume']['mute']).lower()))


	def set_volume(self, cortex: dict, volume: int) -> None:
		cortex['enclosure']['volume']['level'] = volume
		self.daemon.queue_signal('mqtt', {'mqtt': {'topic': 'hal9000/command/kalliope/volume', 'payload': {'level': volume}}})
		self.daemon.logger.info('AUDIO: volume={}'.format(cortex['enclosure']['volume']['level']))

