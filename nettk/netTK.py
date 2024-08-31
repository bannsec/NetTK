#!/usr/bin/env python3 -u

__builtins__.VERSION = "0.1"

import sys

sys.path.append("monitor")

from ping import ping
from database import startHandler
import threading
try:
	from Queue import Queue
except ImportError:
	from queue import Queue
import signal
try:
        from ConfigParser import ConfigParser
except ImportError:
        import configparser
        ConfigParser = lambda : configparser.ConfigParser(inline_comment_prefixes=(';',))

CONFIGFILE = "../netTK.cfg"

def cleanExit():
	"""
	Take care of telling threads to exit and then exiting.
	"""
	# Tell threads we're leaving
	shouldExit.set()

	# Exit cleanly
	sys.exit(0)

def signal_handler(signal, frame):
	"""
	Handle when the user presses ctl-C to exit.
	"""

	# Perform clean exit
	cleanExit()


# Register new abilities here to be callable
dispatcher = {
	'sqlitedb': startHandler, 
	'ping': ping
}

# Register our SIGINT handler
signal.signal(signal.SIGINT, signal_handler)

# Define an addRecord queue
__builtins__.addRecord = Queue()

# Define our exit event to allow threads to cleanly exit
__builtins__.shouldExit = threading.Event()

# Open up our config file
config = ConfigParser()

# Read the config
config.read(CONFIGFILE)

# Loop through the config, starting up whatever we need to.
for section in config._sections:
	# Generate the tag for the module to use
	kargs = dict(config._sections[section])
	kargs["tag"] = kargs["module"].lower()
	if kargs.get("ctag"):
		kargs["tag"] += "_" + kargs["ctag"]

	# Generic thread call. Looks up the "test" paramter (case insensitive) in dispatcher to know what to call.
	t = threading.Thread(target=dispatcher[config._sections[section]["module"].lower()], kwargs=kargs)
	t.start()

# Wait for the user to want to exit
print("Press Enter To Exit\n")
try:
	raw_input()
except NameError:
	input()

# Let the threads know we should be exiting
shouldExit.set()
