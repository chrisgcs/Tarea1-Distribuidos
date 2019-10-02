import socket
import struct
import time
import threading
import _thread
from queue import Queue
import random

def threaded(client, msg_q, node_q):
    out = "Hello i'm server"
    saludo = client.recv(1024)
    print(saludo.decode("utf-8"))
    client.send(out.encode('utf-8'))
    continuar = True
    while(continuar):
        
        nodos = []
        flag = True
        while flag:
            flag = msg_q.empty() #si deja de estar vacio es porque termino el heartbeat
        heartbeat = msg_q.get()
        print(heartbeat)

        # heartbeat_server = open("heartbeat_server.txt","a")
        while not node_q.empty() : 
            node = node_q.get()[0]

            # heartbeat_server.write("respondio: " + node + "\n")

            try:
                print("Nodo agregado = " + node)
            except Exception as exc:
                print(exc)
            
            nodos.append(node)        

        if len(nodos) != 0:
            aviso = "send messages"
            client.send(aviso.encode("utf-8")) #ya puedes mandar los mensajes

            data = client.recv(1024).decode('utf-8') #escuchando mensajes
            nodito = nodos[random.randint(0, len(nodos)-1)] #nodo random

            if (data == "I`m leaving *drops mic*"):
                #print("Ok thank you have a nice day")
                # out = "Ok thank you have a nice day"
                # client.send(out.encode('utf-8'))
                #print_lock.release()
                continuar = False
                break
            print(data)

            message = data
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

            sock.connect((nodito, 6000))  
            
            sock.send(message.encode('utf-8'))
            
            info = sock.recv(1024)
            if info.decode("utf-8") == "registro correcto":
                registro = open("registro_server.txt","a")
                registro.write("El mensaje: [" + message + "] se encuentra en el nodo: [" + nodito + "]\n" )
                registro.close()
            
            reg_cli = "El mensaje: [" + message + "] se encuentra en el nodo: [" + nodito + "]\n"
            client.send(reg_cli.encode("utf-8"))

            # sock.close()
        else:
            aviso = "servicio no disponible, intente en un rato"
            client.send(aviso.encode("utf-8"))

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
            # with node_q.mutex: node_q.queue.clear()
            sent = sock.sendto(message.encode('utf-8'), multicast_group)

            # Look for responses from all recipients
            print('waiting to receive')
            lista = []
            while(True):
                try:
                    data, server = sock.recvfrom(4096)
                    alias = socket.gethostbyaddr(server[0]) #obtengo el nombre del host, ex: node1.network
                    hostip = socket.gethostbyname(alias[0]) #pruebo que efectivamente nodeX.network me de su ip
                    print(alias) #uwu
                    print(hostip) #unu
                    node_q.put(alias)
                    lista.append(alias[0])
                    

                    print('received {!r} from {}'.format(data.decode('utf-8'), server))
                except:
                    print("No more nodes sent ACK")
                    break
            msg_q.put("heartbeat done")
            heartbeat_server = open("heartbeat_server.txt","a")
            for i in lista:
                heartbeat_server.write("respondio: " + i + "\n")
            heartbeat_server.close()
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