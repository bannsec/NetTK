import socket
import time

def tcpping(host, port, alias, tag, delay=1, timeout=1, addRecord=None, shouldExit=None, **args):
    """
    Input:
        Associative array containing the following args. (i.e.: {"host": "example.com", "port": 80, "alias": "MyServer"})
        host = host to monitor (i.e.: "example.com" or "192.168.1.1")
        port = port to monitor (i.e.: 80)
        alias = alias to give this host. This will be used in creating the table name (i.e.: "MyServer")
        tag = tag for saving information. provided by the framework
        (optional) delay = time delay in seconds between attempts to contact the host (i.e.: "1" without quotes for 1 second delays)
        (optional) timeout = how long to wait for a reply to the ping in seconds. defaults to 1 second.
        (optional) addRecord = Queue for adding records
        (optional) shouldExit = Event to signal when to exit

    Action:
        TCP ping the host continuously until told to stop. Records packet delay time and dropped packets.

    Returns:
        Nothing
    """

    # Sanitize the input a little
    delay = int(delay)
    timeout = int(timeout)
    TAG = tag

    while True:
        # Check if we should be exiting
        if shouldExit.isSet():
            return

        time.sleep(delay)

        start_time = time.time()
        try:
            sock = socket.create_connection((host, port), timeout)
            sock.close()
            end_time = time.time()
            delta = end_time - start_time
            addRecord.put({'timeStamp': start_time, 'delayTime': delta, 'tableName': alias + "_" + TAG, 'isDroppedPacket': 0})
        except socket.error:
            end_time = time.time()
            addRecord.put({'timeStamp': start_time, 'delayTime': None, 'tableName': alias + "_" + TAG, 'isDroppedPacket': 1})

if __name__ == "__main__":
    print("This isn't meant to be called directly.")
