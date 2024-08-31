#!/usr/bin/env python

import sys
import os
from nettk.version import VERSION

sys.path.append("analysis")
sys.path.append("monitor")

from lineGraph import lineGraphRun
from pieChart import pieChartRun
from multiprocessing import Process
try:
        from ConfigParser import ConfigParser
except ImportError:
        import configparser
        ConfigParser = lambda : configparser.ConfigParser(inline_comment_prefixes=(';',))
from database import connectDB

script_dir = os.path.dirname(os.path.abspath(__file__))
CONFIGFILE = os.path.join(script_dir, "../netTKAnalysis.cfg")

# Register new abilities here to be callable
# Remember the keys here should be lowercase
dispatcher = {
	'linegraph -- latency': lineGraphRun, 
	'piechart -- dropped packets': pieChartRun
}

def main():
    # Open up our config file
    config = ConfigParser()

    # Read the config
    config.read(CONFIGFILE)

    # Loop through the config, starting up whatever we need to.
    for section in config._sections:

        # Special case of connecting to DB
        # TODO: Need to have better way of handling the db...
        if section == "SQLite Database Handler":
            connectDB(config._sections[section]["dbname"])
            continue

        # Index to keep track of multiple graphs per section
        i = 1

        # standardize the dict to a normal dict
        kargs = dict(config._sections[section])

        # Loop through the plots
        while "alias_%s" % i in kargs:
            tag = "tag_%s" % i
            ctag = "vtag_%s" % i
            module =  "module_%s" % i
            # Set tag = "<module_i>
            kargs[tag] = kargs[module].lower()

            # If there's a custom ctag, add it to the tag
            if kargs.get(ctag):
                kargs[tag] += "_" + kargs[ctag]

            # Increment the index
            i += 1

        # Generic thread call. Looks up the "section" paramter (case insensitive) in dispatcher to know what to call.
        #t = threading.Thread(target=dispatcher[section.lower()], kwargs=kargs)
        p = Process(target=dispatcher[section.lower()], kwargs=kargs)

        # Nothing should be damaged with allowing these to daemonize
        p.daemon = True

        # Start it
        p.start()

    # Wait for the user to want to exit
    print("Press Enter To Exit\n")
    try:
            raw_input()
    except NameError:
            input()

if __name__ == "__main__":
    main()
