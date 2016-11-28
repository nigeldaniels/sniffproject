#!/usr/bin/python2

"""
Usage:
    myshit [options]
    myshit --scan-local <port>
    myshit -d
    myshit --scan-ip <host>

Options:
    --scan-local    s cans the current subnet for other hosts.
    -d              run in dameon mode
    --scan-ip       scans one ip
"""


import socket 
import Queue
from pyroute2 import IPDB
from pyroute2 import IPRoute 
import signal
import threading
import time
import select
from docopt import docopt

work_queue = Queue.Queue()
ip = IPDB()
JUNK_DATA = "AAABBBCCC"


class Worker(threading.Thread):
    def run(self):
        while True:
            msg = work_queue.get()
        if msg['event'] == 'RTM_NEWLINK':
            plugin(msg)


#when you plug in an the ethernet adapter we get the ip of the interface
def plugin(msg):
    interface =  msg['attrs'][0][1]
    state     =  msg['attrs'][2][1]           
    print interface + ":" + state   
   
    if state == "UP":
        while not get_ip(interface): 
            time.sleep(1)
        ip_msg = get_ip(interface)
        ip_addr = ip_msg[0]['attrs'][1][1]
        ip_broadcast = ip_msg[0]['attrs'][2][1]
        print ip_addr  
        time.sleep(2)
        simple_tcp_scan(fix_broadcast(ip_broadcast),ip_broadcast) 


def simple_tcp_scan(fixed_broadcast, ip_broadcast):
    start_host=fixed_broadcast 
    target_port = 80
    
    ip_range = ipRange(fixed_broadcast, ip_broadcast)
    for ip in ip_range:
        print ip
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip,target_port)) 
            client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
            response = client.recv(4096)
            print response  
        except IOError as e:
            print "ass"


def simple_udp_scan(ip_range, port):
    for ip in ip_range:
        print ip
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.sendto(JUNK_DATA, (ip, port))
            ready = select.select([client], [], [], 3)
            if ready[0]:
                data, addr = client.recvfrom(4096)
                print data
            else:
                print "timeout waiting for response"
        except IOError as e:
            print "error"


def scan_ip_udp(ip):
        port = 12
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.sendto(JUNK_DATA, (ip, port))
            data, addr = client.recvfrom(4096)
            print data
        except IOError as e:
            print "error"


def ipRange(start_ip, end_ip):
   start = list(map(int, start_ip.split(".")))
   end = list(map(int, end_ip.split(".")))
   temp = start
   ip_range = []  
   
   ip_range.append(start_ip)
   while temp != end:
      start[3] += 1
      for i in (3, 2, 1):
         if temp[i] == 256:
            temp[i] = 0
            temp[i-1] += 1
      ip_range.append(".".join(map(str, temp))) 

   return ip_range


def fix_broadcast(ip_broadcast):
    broadcast_array = ip_broadcast.split('.') 
    for n, octect in enumerate(broadcast_array):
        if octect == '255':
           broadcast_array[n] = '0'
    broadcast_ip = '.'.join(broadcast_array)
    return broadcast_ip 
    

def get_ip(interface):
    ipr = IPRoute()
    return ipr.get_addr(label=interface) 


def get_ip_simple():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    return s.getsockname()[0]

# POSIX signal handler to ensure we shutdown cleanly   

def handler(signum, frame):
    print "\nShutting down IPDB instance..."
    ip.release()


# Called by the IPDB Netlink listener thread for _every_ message (route, neigh, etc,...)
def callback(ipdb, msg, action):
        work_queue.put(msg)


def daemon():
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    # Worker thread
    worker = Worker()
    worker.daemon = True
    worker.start()
    # Register our callback to the IPDB
    ip.register_callback(callback)
    # The process main thread does nothing but waiting for signals
    signal.pause()


def main():
    args = docopt(__doc__, version="myshit 1.0")

    if args['-d']:
        daemon()

    if args['--scan-local']:
        ip = get_ip_simple()
        tempip = ip.split(".")
        tempip[3] = 0
        print tempip
        myip = ".".join(str(e) for e in tempip)
        tempip[3] = 255
        endip = ".".join(str(e) for e in tempip)

        simple_udp_scan(ipRange(myip, endip), int(args['<port>']))

    if args['--scan-ip']:
        scan_ip_udp(args['<host>'])



if __name__ == '__main__':
    main()
