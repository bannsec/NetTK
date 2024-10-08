#!/usr/bin/env python3 -u

import sys
import os
from nettk.version import VERSION

sys.path.append("monitor")

from ping import ping
from tcpping import tcpping
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

script_dir = os.path.dirname(os.path.abspath(__file__))
CONFIGFILE = os.path.join(script_dir, "../netTK.cfg")

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
	'ping': ping,
	'tcpping': tcpping
}

def main():
	# Check if running as root
	if os.geteuid() != 0:
		print("This script needs to be run as root. Re-running with sudo...")
		os.execvp("sudo", ["sudo", "-E"] + sys.argv)

	# Register our SIGINT handler
	signal.signal(signal.SIGINT, signal_handler)

	# Define an addRecord queue
	addRecord = Queue()

	# Define our exit event to allow threads to cleanly exit
	shouldExit = threading.Event()

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

		# Add addRecord and shouldExit to kargs
		kargs["addRecord"] = addRecord
		kargs["shouldExit"] = shouldExit

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

if __name__ == "__main__":
	main()
