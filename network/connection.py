""""
https://pynetworktables.readthedocs.io/en/latest/examples.html#pynetworktables-examples

"""

import threading
from networktables import NetworkTables
import config

cond = threading.Condition()
notified = [False]

_dashboard = None

# start networktables connection
def init(remote=True):
    global _dashboard

    # sub function to block anything from happening until
    # Networktable connection is established
    # only required if ip is not localhost

    def connectionListener(connected, info):
        print(info, '; Connected=%s' % connected)
        # TODO: if connection is terminated, we should exit program
        with cond:
            notified[0] = True
            cond.notify()

    NetworkTables.initialize()
    if remote is True or config.networktables_server_ip != '127.0.0.1':
        NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
        with cond:
            print("Waiting for NetworkTables on %s" % config.networktables_server_ip)
            if not notified[0]:
                cond.wait()

    else:
        print('Starting local version of NetworkTables')

    print("SmartDashboard ready")
    _dashboard = NetworkTables.getTable(config.networktables_table)
#

def get():
    return _dashboard