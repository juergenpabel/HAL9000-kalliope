#!/usr/bin/python3

from webserial import webserial
import json

commands = None


def handler(host: webserial, line: str):
	if line is not None:
		topic, body = json.loads(line)
		if topic in commands:
			commands[topic](host, topic, body)


def application_runtime(host: webserial, topic: str, payload):
	if "status" in payload:
		if payload["status"] == "?":
			host.send(json.dumps([topic, {"status": host.application_runtime["status"]}]))
		else:
			host.application_status = payload["status"]


commands = dict()
commands["application/runtime"] = application_runtime

try:
	host = webserial(False, True)
	host.connect()
	host.application_runtime = dict()
	host.application_runtime["status"] = "running"
	host.run(handler)
except KeyboardInterrupt:
	pass

