#!/usr/bin/env python3

import sqlite3
from threading import Thread, Lock

# Name of the sqlite database file
DATABASE = "NetTK.db"

# Define our mutex
mutex = Lock()

# Holders for our stuff
c = None
conn = None

####################
# Define the schema 
####################

# This is the quick template for adding a table with variable already there
createTable = """
CREATE TABLE {0} (
        timeStamp time PRIMARY KEY NOT NULL,
        isDroppedPacket integer NOT NULL,
        delayTime real,

        /* Checks */
        /* Make sure we are using isDroppedPacket is a boolean */
        CHECK (isDroppedPacket IN ("0", "1"))
);
"""
# This is the sqlite statement to insert a new row
insertRecord = """
INSERT INTO {0} (timeStamp, isDroppedPacket, delayTime) VALUES (?, ?, ?);
"""

def connectDB(dbName):
	"""
	Input:
		dbName = sqlite database name to use (i.e.: NetTK.db)
	Action:
		Opens database if it exists, creates it if it doesn't.
		Populated global variables of conn (sqlite connection) and c (sqlite cursor)
	Return:
		Nothing
	"""
	global conn, c

	# Open the database, creating if needed
	conn = sqlite3.connect(dbName, check_same_thread=False)

	# Create our cursor
	c = conn.cursor()


# Standard name and arguments for adding a record (i.e.: saving what happened with an individual test)
# This could be replaced with any way that you would like to store this information
def saveRecord(tableName, timeStamp, isDroppedPacket, delayTime):
	"""
	Input:
		tableName = name of the table (i.e.: "Google.ping")
		timeStamp = Unix epoc time in UTC for when this event occured. Generally, this will be when the test packet was sent. (i.e.: "1403217490.87")
		isDroppedPacket = Either 1 or 0 to note if the packet in question was dropped. 1 == packet was dropped, 0 == packet was not dropped. If the packet was dropped, the delayTime should be NULL
		delayTime = Time in seconds that it took for the packet to return.
	Action:
		Save the information. This implementation will save it to a sqlite database.
		If the database or table doesn't already exist, it will be created automatically.
	Returns:
		Nothing.
	"""

	# For safety, only one thing should be updating this at a time
	with mutex:
	
		# Wrapping this insert in a try statement so that we add tables on the fly as needed
		try:
			c.execute(insertRecord.format(tableName), (timeStamp, isDroppedPacket, delayTime))

		except sqlite3.OperationalError as e:

			# Lets make sure this is the error we're looking for
			if "no such table:" in str(e).lower():
				# Create this table on the fly
				c.execute(createTable.format(tableName))

				# Now try adding again
				c.execute(insertRecord.format(tableName), (timeStamp, isDroppedPacket, delayTime))
	
			else:
				# We must have caught something we didn't mean to. Lets be nice and forward it along
				raise e

		# If we've gotten this far, lets save our progress
		conn.commit()

def getRows(table, age=None):
	"""
	Input:
		table = Name of table to grab data from (i.e.: "Google_PING")
		age (optional) = Get data of a certain age (i.e.: "1 seconds", "2 minutes", "3 hours", "4 days", "5 months", "6 years")
			This defaults to all data
	Action:
		Grabs timeStamp, droppedpacket, and delay information. Parses it into flat array for use in plotting.
	Returns:
		Tuple of flat arrays of timestamp, isdroppedpacket, delay times. (i.e.: ([1234567.8675, 1215245234.34234], [0,0], [0.12314,0.1234352]))
	"""

	# Define our default where clause
	WHERE = "1 == 1;"

	# If we want to add an age modifier
	if age is not None:
		WHERE = "timeStamp >= strftime('%s','now','-{0}')".format(age)
		# SELECT datetime(timeStamp, 'unixepoch', 'localtime') from Google_PING WHERE timeStamp >= strftime('%s','now','-3.5 hours');

	# Grab timestamps
	# Making this a hack for now due to getting "database is locked" errors periodically.
	# TODO: Re-arrange how the database is calledso we don't get databased locked errors.
	try:
		c.execute("SELECT timeStamp,isDroppedPacket,delayTime FROM {0} WHERE {1};".format(table,WHERE))
	except sqlite3.OperationalError as e:
		if "database is locked" in str(e).lower():
			# Looks like we hit our db locked problem. Lets give it one more shot to work
			c.execute("SELECT timeStamp,isDroppedPacket,delayTime FROM {0} WHERE {1};".format(table,WHERE))
		else:
			# Other problem came up. Forward it up the chain.
			raise e

	# Grab all the rows
	all = c.fetchall()

	# Break out the results
	timeStamps = [row[0] for row in all]
	isDroppedPackets = [row[1] for row in all]
	delayTimes = [row[2] for row in all]

	# Return as a tuple
	return (timeStamps, isDroppedPackets, delayTimes)



def startHandler(dbname, addRecord, shouldExit, **kwargs):
	"""
	Input:
		dbname = Name of the sqlite database file to use. Will be created if it doesn't exist (i.e.: NetTK.db)
		addRecord = Queue for adding records
		shouldExit = Event to signal when to exit
	Action:
		Shim function to watch for new items in the addRecord queue, and then call the addRecord function
		Record should look like {'timeStamp': 12345676.1234, 'delayTime': 0.55123145, 'tableName': 'Google_PING', 'isDroppedPacket': 0}
	Returns:
		Nothing
	"""

	# Connect to the database
	connectDB(dbname)

	while True:
		# Grab the next item to save
		record = addRecord.get()

		# Call the process to add the record
		saveRecord(record["tableName"], record["timeStamp"], record["isDroppedPacket"], record["delayTime"])

		# Be nice and let the queue know it's done
		addRecord.task_done()

		# Check if we should be exiting
		if shouldExit.isSet():
			return
