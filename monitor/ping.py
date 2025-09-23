#!/usr/bin/env python3 -u
from scapy.all import *
from time import sleep, time
from nettk.version import VERSION

def ping(host, alias, tag , delay=1, timeout=1, addRecord=None, shouldExit=None, **args):
  """
	Input:
		Associative array containing the following args. (i.e.: {"host": "Google.com", "alias": "Google"})
		host = host to monitor (i.e.: "google.com" or "192.168.1.1")
		alias = alias to give this host. This will be used in creating the table name (i.e.: "Google")
		tag = tag for saving information. provided by the framework
		(optional) delay = time delay in seconds between attempts to contact the host (i.e.: "1" without quotes for 1 second delays)
		(optional) timeout = how long to wait for a reply to the ping in seconds. defaults to 1 second.
		(optional) addRecord = Queue for adding records
		(optional) shouldExit = Event to signal when to exit

	Action:
		Ping's the host continuously until told to stop. Records packet delay time and dropped packets.

	Returns:
		Nothing
  """

  # Sanitize the input a little
  delay = int(delay)
  timeout = int(timeout)
  TAG = tag

  packet = Ether()/IP(dst=host)/ICMP()/"NetTK v{0} https://github.com/bannsec/NetTK".format(VERSION)

  while True:
      # Check if we should be exiting
      if shouldExit.isSet():
           return

      sleep(delay)

      start_time = time()
      ans, unans = srp(packet, verbose=0, timeout=timeout, retry=0, multi=0)
      if len(ans) == 0:
        # Save this as a dropped packet
        addRecord.put({'timeStamp': start_time, 'delayTime': None, 'tableName': alias + "_" + TAG, 'isDroppedPacket': 1})
        continue

      # Time received
      rx = ans[0][1]

      # Compute the latency (fallback if rx.time is missing)
      if hasattr(rx, "time") and isinstance(rx.time, (int, float)):
          delta = rx.time - start_time
      else:
          delta = time() - start_time

      # Save this information to the database
      addRecord.put({'timeStamp': start_time, 'delayTime': delta, 'tableName': alias + "_" + TAG, 'isDroppedPacket': 0})

if __name__=="__main__":
      print("This isn't meant to be called directly.")
