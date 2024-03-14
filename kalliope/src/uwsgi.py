#!/usr/bin/env python3
import sys

import kalliope
try:
	from uwsgi import accepting
	accepting()
except ImportError:
	pass

sys.argv[0] = 'kalliope'
sys.argv.append('--debug')
sys.argv.append('start')
sys.exit(kalliope.main())

