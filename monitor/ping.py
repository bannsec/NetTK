#!/usr/bin/python -u
from scapy.all import *
from time import sleep

def ping(host, alias, tag , delay=1, timeout=1, **args):
  """
	Input:
		Associative array containing the following args. (i.e.: {"host": "Google.com", "alias": "Google"})
		host = host to monitor (i.e.: "google.com" or "192.168.1.1")
		alias = alias to give this host. This will be used in creating the table name (i.e.: "Google")
		tag = tag for saving information. provided by the framework
		(optional) delay = time delay in seconds between attempts to contact the host (i.e.: "1" without quotes for 1 second delays)
		(optional) timeout = how long to wait for a reply to the ping in seconds. defaults to 1 second.

	Action:
		Ping's the host continuously until told to stop. Records packet delay time and dropped packets.

	Returns:
		Nothing
  """

  # Sanitize the input a little
  delay = int(delay)
  timeout = int(timeout)
  TAG = tag

  packet = Ether()/IP(dst=host)/ICMP()/"NetTK v{0} https://github.com/Owlz/NetTK".format(VERSION)

  while True:
      # Check if we should be exiting
      if shouldExit.isSet():
           return

      sleep(delay)

      ans,unans=srp(packet, verbose=0, timeout=1, retry=0, multi=0)
      if len(ans) == 0:
        # Save this as a dropped packet
        addRecord.put({'timeStamp': unans[0][0].sent_time, 'delayTime': None, 'tableName': alias + "_" + TAG, 'isDroppedPacket': 1})
        continue

      # Time received and time sent
      rx = ans[0][1]
      tx = ans[0][0]

      # Compute the latency
      delta = rx.time-tx.sent_time

      # Save this information to the database
      addRecord.put({'timeStamp': ans[0][0].sent_time, 'delayTime': delta, 'tableName': alias + "_" + TAG, 'isDroppedPacket': 0})

if __name__=="__main__":
      print "This isn't meant to be called directly."
