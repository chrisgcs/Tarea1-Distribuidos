import socket
import struct
import time
import threading
import _thread
from queue import Queue
import random

def threaded(client, msg_q, node_q):
    out = "Hello i'm server"
    client.send(out.encode('utf-8'))
    while(True):
        data = client.recv(1024).decode('utf-8')
        nodos = []
        while not node_q.empty() : 
            nodos.append(node_q.get())
        nodito = nodos[random.randint(0, len(nodos))]

        message = data
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

        sock.connect((nodito, 6000))  ###################################
        # hay que ver bien el tema de cual puerto se usara para evitar conflictos
        sock.send(message.encode('utf-8'))
        
        data = sock.recv(1024)
        if data.decode("utf-8") == "registro correcto":
            registro = open("registro_server.txt","a")
            registro.write("El mensaje: [" + message + "] se encuentra en el nodo: [" + nodito + "]\n" )
            registro.close()
        
        reg_cli = "El mensaje: [" + message + "] se encuentra en el nodo: [" + nodito + "]\n"
        client.send(reg_cli.encode("utf-8"))

        if (data == "I`m leaving *drops mic*"):
            #print("Ok thank you have a nice day")
            out = "Ok thank you have a nice day"
            client.send(out.encode('utf-8'))
            #print_lock.release()
            break
        print(data)
    client.close()

def thread_nodes(msg_q, node_q):
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
    print(socket.gethostbyname(socket.gethostname()))

    sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton("172.18.18.2"))
    #AQUI LE DEFINO LA INTERFAZ QUE QUIERO PARA LOS NODOS
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
                    node_q.put(alias)
                    print('received {!r} from {}'.format(data.decode('utf-8'), server))
                except:
                    print("No more nodes sent ACK")
                    break
    finally:
        print('closing socket')
        sock.close()

def Main():
    msg_q = Queue()
    node_q = Queue()

    _thread.start_new_thread(thread_nodes, (msg_q, node_q, ) )

    host = ""
    port = 5000
    print(socket.gethostbyname(socket.gethostname()))
    sock = socket.socket()
    sock.bind((host, port))
    print("Binded to port ", port)

    sock.listen(5)
    print("Socket Listening")

    while True:
        client, addrs = sock.accept()
        #print_lock.acquire()
        print("Connected to: ", addrs[0], ":", addrs[1])
        _thread.start_new_thread(threaded, (client, msg_q, node_q, ) )
    sock.close()

if __name__ == '__main__':
    Main()