import socket
import struct
import time

message = 'very important data'
multicast_group = ('224.10.10.10', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
sock.settimeout(5)

# Set the time-to-live for messages to 1 so they do not
# go past the local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:
    while True:
        # Send data to the multicast group
        print('sending {!r}'.format(message))
        sent = sock.sendto(message.encode('utf-8'), multicast_group)

        # Look for responses from all recipients
        print('waiting to receive')
        while(True):
            try:
                data, server = sock.recvfrom(4096)
                alias = socket.gethostbyaddr(server[0]) #obtengo el nombre del host, ex: node1.network
                hostip = socket.gethostbyname(alias[0]) #pruebo que efectivamente nodeX.network me de su ip
                print(alias) #uwu
                print(hostip) #unu
                print('received {!r} from {}'.format(data.decode('utf-8'), server))
            except:
                print("No more nodes sent ACK")
                break
finally:
    print('closing socket')
    sock.close()