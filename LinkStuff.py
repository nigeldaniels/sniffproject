import os
import socket
import struct
from pyroute2 import IPDB
from pyroute2.ipdb import get_addr_nla
# from pyroute2.common import
from pyroute2.netlink.rtnl import RTM_NEWLINK

ip = IPDB()
def callback(ipdb, msg, action):
    values = {}
    # Only care if we have a new link
    if action == 'RTM_NEWLINK':
        interface = msg.get_attr('IFLA_IFNAME')
        # ipdb.interfaces[interface]['ipaddr'] is an instance of IPaddrSet from linkedset.py in pyroute2 library
        # This check is not working 100%. Sometimes it goes in the if statement when there is nothing in the set
        if ipdb.interfaces[interface]['ipaddr']:
            print("Mac Adress: ", ipdb.interfaces[interface]['address'])
            print("Broadcast address: ", ipdb.interfaces[interface]['broadcast'])
            # Trying to get the correct ip address and netmask doesnt work all the time
            # When you have an ip address and do a 'sudo ip link set <ifname> down', it will cause an exception
            # print("IP address: ", ipdb.interfaces[interface]['ipaddr'][1]['address'])

if __name__ == '__main__':
    ip.register_callback(callback)
    while True:
        pass

