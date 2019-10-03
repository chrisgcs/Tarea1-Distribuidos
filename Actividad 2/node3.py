import socket
import struct
import sys
import time
import threading
import _thread


def threaded(client): #Funcion que maneja el thread donde se registran los mensajes del cliente
    data = client.recv(1024).decode('utf-8')
    data_file = open(r"/usr/src/app/node3/data.txt","a")
    print(data)
    data_file.write("%s\n" % data)
    data_file.close()

    succes = "Registro correcto"
    try:
        client.send(succes.encode('utf-8'))
    except socket.error as e:
        print(e)
    except IOError as e:
        if e == EPIPE:
            print(e)
        else:
            print("not EPIPE")
    client.close()

def thread_nodes(): #Funcion que maneja el thread encargado de responder al heartbeat
    multicast_group = '224.10.10.10'
    server_address = ('0.0.0.0', 10000)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    sock.bind(server_address)

    group = socket.inet_aton(multicast_group)+socket.inet_aton("172.18.18.1") #Recibe de esta interfaz
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        mreq)

    while True:
        print('\nwaiting to receive message')
        data, address = sock.recvfrom(1024)

        print('received {} bytes from {}'.format(
            len(data), address))
        print(data.decode('utf-8'))

        print('sending acknowledgement to', address)
        sock.sendto('ack'.encode('utf-8'), address)

def Main():
    _thread.start_new_thread(thread_nodes, ())

    host = ""
    port = 6000
    sock = socket.socket()
    sock.bind((host, port))
    print("Binded to port ", port)

    sock.listen(5)
    print("Socket Listening")

    while True:
        client, addrs = sock.accept()
        print("Connected to: ", addrs[0], ":", addrs[1])

        _thread.start_new_thread(threaded, (client, ) )
    sock.close()

if __name__ == '__main__':
    Main()