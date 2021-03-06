#!/usr/bin/python3

import os
import sys
import time
from threading import Thread
from configparser import ConfigParser

#from uwsgi import accepting


config = ConfigParser(delimiters='=', converters={'list': lambda list: [item.strip() for item in list.split(',')]})
config.read(sys.argv[1])
module_paths = config.getlist('python', 'module-paths', fallback=['.'])
for module_path in module_paths:
	sys.path.append(module_path.strip('"').strip("'"))


from hal9000.brain.daemon import Daemon

daemon = Daemon()
daemon.load(sys.argv[1])

#accepting()
while True:
	daemon.loop()

