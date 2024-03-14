import json
import flet_core

from . import ScreenKalliope


class ScreenStatus(ScreenKalliope):

	targets = {
		   'version': { 'type': 'readonly', 'icon': flet_core.icons.INFO, 'text': 'Kalliope version',
	                        'target:jsonpath': '$.settings.kalliope_version', 'target:api-identifier': None },
		   'mute':    { 'type': 'bool',     'text': 'Speaker status',
	                        'target:jsonpath': '$.settings.options.mute',     'target:api-identifier': 'mute',
	                        'icons': { 'True': flet_core.icons.VOLUME_OFF, 'False': flet_core.icons.VOLUME_UP } },
		   'deaf':    { 'type': 'bool',     'text': 'Microphone status',
	                        'target:jsonpath': '$.settings.options.deaf',     'target:api-identifier': 'deaf',
	                        'icons': { 'True': flet_core.icons.MIC_OFF, 'False': flet_core.icons.MIC } },
	       }
	target_parameters = {
	}


	def __init__(self):
		super().__init__("Status", False, 'http://127.0.0.1:5000/settings')


	def load_data(self):
		try:
			return super().load_data()
		except Exception:
			self.data = {}
		return False


	def save_data(self, name, value):
		result = False
		if name is not None:
			try:
				result = super().save_data(name, value)
			except Exception as e:
				#TODO logging
				pass
		return result

