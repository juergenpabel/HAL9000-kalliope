#!/usr/bin/env python3

import logging
import json
from configparser import ConfigParser

import asyncio
import serial_asyncio


class Webserial:

	def __init__(self):
		self.logger = logging.getLogger()
		self.config = dict()


	def configure(self, configuration: ConfigParser) -> None:
		self.config['webserial:trace']  = configuration.getboolean('webserial', 'trace', fallback=False)
		self.config['webserial:device'] = configuration.getstring('webserial', 'device', fallback='/dev/ttyHAL9000')
		self.config['mcp23X17:i2c-bus']     = configuration.getint('mcp23X17', 'i2c-bus',     fallback=0)
		self.config['mcp23X17:i2c-address'] = configuration.getint('mcp23X17', 'i2c-address', fallback=32)

		self.config['mcp23X17:peripherals'] = configuration.getlist('mcp23X17', 'peripherals', fallback=[])
		for peripheral in self.config['mcp23X17:peripherals']:
			peripheral_type, peripheral_name = peripheral.split(':', 1)
			if peripheral_type in ["rotary"]:
				input_pins = configuration.getlist(peripheral, 'mcp23X17-pins', fallback=[])
				if type(input_pins) == list and len(input_pins) == 2:
					self.config[f"{peripheral}:mcp23X17-pins"] = input_pins
				else:
					self.logger.error(f"invalid configuration in section '{peripheral}' for option 'mcp23X17-pins': must be a list with exactly two pin names")
#TODO					return
			if peripheral_type in ["switch", "button", "toggle"]:
				input_pin = configuration.get(peripheral, 'mcp23X17-pin', fallback="")
				if type(input_pin) == str and len(input_pin) == 2:
					self.config[f"{peripheral}:mcp23X17-pin"]    = input_pin
					self.config[f"{peripheral}:mcp23X17-pullup"] = configuration.getboolean(peripheral, 'mcp23X17-pullup', fallback=True)
					self.config[f"{peripheral}:event-low"]       = configuration.getstring(peripheral, 'event-low', fallback='on')
					self.config[f"{peripheral}:event-high"]      = configuration.getstring(peripheral, 'event-high', fallback='off')
				else:
					self.logger.error(f"invalid configuration in section '{peripheral}' for option 'mcp23X17-pin': must be a single pin name (A0-A7,B0-B7)")
#TODO					return
				

	async def recv(self) -> str:
		bytes = await self.source_reader.readline()
		line = bytes.decode('utf-8').strip()
		if self.config['webserial:trace'] is True:
			self.logger.debug(f"USB(D->H): {line}")
		return line


	async def send(self, topic: str, payload, quote_payload: bool = False) -> None:
		if type(payload) == str and quote_payload is True:
			payload = payload.replace('"', '\\"')
			payload = f"\"{payload}\""
		if type(payload) == dict:
			payload = json.dumps(payload)
		line = f"[\"{topic}\", {payload}]"
		line = line.strip()
		if self.config['webserial:trace'] is True:
			self.logger.debug(f"USB(H->D): {line}")
		self.source_writer.write(f"{line}\n".encode('utf-8'))
		await self.source_writer.drain()


	async def loop(self, target_writer):
		self.logger.info(f"webserial => Connecting to '{self.config['webserial:device']}'...")
		self.source_reader, self.source_writer = await serial_asyncio.open_serial_connection(url=self.config['webserial:device'], baudrate=115200)
		await self.send("application:runtime", {"status":"?"})
		runtime = {}
		while "status" not in runtime or runtime["status"] == "booting":
			line = await self.recv()
			try:
				message = json.loads(line)
				if type(message) == list and len(message) == 2:
					if message[0] == "application:runtime":
						runtime = message[1]
			except BaseException as e:
				self.logger.debug(f"json.loads({line}) raised this exception:")
				self.logger.error(str(e))
				self.logger.error(type(e))
		if runtime["status"] == "configuring":
			await self.send('["device:mcp23X17", {"init":{"i2c-bus":%d,"i2c-address":%d}}]' % (self.config['mcp23X17:i2c-bus'], self.config['mcp23X17:i2c-address']))
			for peripheral in self.config['mcp23X17:peripherals']:
				peripheral_type, peripheral_name = peripheral.split(':', 1)
				peripheral_pins = self.config[f"{peripheral}:mcp23X17-pins"]
				if peripheral_type in ["rotary"]:
					await self.send('["device:mcp23X17", {"config":{"device":{"type":"%s","name":"%s","inputs":[{"pin":"%s","label":"sigA"},{"pin":"%s","label":"sigB"}]}}}]'
					                %(peripheral_type, peripheral_name, input_pins[0], input_pins[1]))
				if peripheral_type in ["switch", "button", "toggle"]:
					input_pin    = self.config[f"{peripheral}:mcp23X17-pin"]
					input_pullup = self.config[f"{peripheral}:mcp23X17-pullup"]
					event_low    = self.config[f"{peripheral}:event-low"]
					event_high   = self.config[f"{peripheral}:event-high"]
					await self.send('["device:mcp23X17", {"config":{"device":{"type":"%s","name":"%s","inputs":[{"pin":"%s","pullup":"%s","label":"sigX"}]'
					                                                                                ',"events":{"low":"%s","high":"%s"}}}}]'
					                %(peripheral_type, peripheral_name, input_pin, str(input_pullup).lower(), event_low, event_high))
			await self.send("device:mcp23X17", {"start":true})
			await self.send('["", ""]')
		await self.send("application:runtime", {"status":"?"})
		while True:
			line = await self.recv()
			try:
				message = json.loads(line)
				if type(message) == list and len(message) == 2:
					topic   = message[0]
					payload = message[1]

					if topic.startswith("syslog:"):
						log_level = logging.WARN
						syslog, level = topic.split(':', 1)
						if isinstance(level, str):
							if hasattr(logging, level.upper()):
								log_level = getattr(logging, level.upper())
						self.logger.log(log_level, payload)
					elif topic == "application:runtime" and 'status' in payload:
						if payload["status"] == "running":
							await target_writer.send("webserial:state", "online")
						if payload["status"] in ["resetting", "halting"]:
							await target_writer.send("webserial:state", "offline")
					elif topic == "application:event" and 'error' in payload:
						await target_writer.send("gui:error", payload)
					elif topic == "gui:event" and 'screen' in payload:
						await target_writer.send("gui:screen", payload)
					elif topic == "device:event" and 'device' in payload:
						device_type=payload["device"]["type"]
						device_name=payload["device"]["name"]
						if device_type in ["rotary"]:
							await target_writer.send(f"{device_type}:{device_name}", f"{device_type}:{device_name} delta={payload['event']['delta']}")
						if device_type in ["switch", "button", "toggle"]:
							await target_writer.send(f"{device_type}:{device_name}", f"{device_type}:{device_name} status={payload['event']['status']}")
					else:
						await target_writer.send(topic, payload)
			except BaseException as e:
				self.logger.debug(f"json.loads({line}) raised this exception:")
				self.logger.error(str(e))
				self.logger.error(type(e))
