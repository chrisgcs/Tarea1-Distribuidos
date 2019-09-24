import socket
import struct
import sys
import time
import threading
import _thread


def thread_nodes():
    multicast_group = '224.10.10.10'
    server_address = ('0.0.0.0', 10000)

    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    # Bind to the server address
    sock.bind(server_address)

    # Tell the operating system to add the socket to
    # the multicast group on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        mreq)

    # Receive/respond loop
    while True:
        print('\nwaiting to receive message')
        data, address = sock.recvfrom(1024)

        print('received {} bytes from {}'.format(
            len(data), address))
        print(data.decode('utf-8'))

        print('sending acknowledgement to', address)
        sock.sendto('ack'.encode('utf-8'), address)
        
        #data, address = sock.recvfrom(1024)
        #if(data):
        #    print("Success")

def Main():
    _thread.start_new_thread(thread_nodes, ())
    while True:
        print("still alive")
        time.sleep(5)

if __name__ == '__main__':
    Main()