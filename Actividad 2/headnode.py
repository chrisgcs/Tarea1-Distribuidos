import socket
import struct
import time
import threading
import _thread
from queue import Queue
import random

def threaded(client, msg_q, node_q):
    out = "Hola, soy el servidor"
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

            if (data == "Adios"):
                continuar = False
                break
            print(data)

            message = data
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

            sock.connect((nodito, 6000))  
            
            sock.send(message.encode('utf-8'))
            
            info = sock.recv(1024)
            if info.decode("utf-8") == "registro correcto":
                registro = open(r"/usr/src/app/server/registro_server.txt","a")
                registro.write("El mensaje: [" + message + "] se encuentra en el nodo: [" + nodito + "]\n" )
                registro.close()
            
            reg_cli = "El mensaje: [" + message + "] se encuentra en el nodo: [" + nodito + "]\n"
            client.send(reg_cli.encode("utf-8"))
        else:
            aviso = "Servicio no disponible, intente en un rato"
            client.send(aviso.encode("utf-8"))

    client.close()

def thread_nodes(msg_q, node_q):
    message = 'Heartbeat data'
    multicast_group = ('224.10.10.10', 10000)

    #Crear el socket datagram
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Definir el timeout, el cual sera utilizado para implementar el heartbeat
    sock.settimeout(5)

    # Se define el tiempo de vida (time to live) del segmento para que no salte de la red local
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    print(socket.gethostbyname(socket.gethostname()))

    sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton("172.18.18.2"))
    #AQUI LE DEFINO LA INTERFAZ QUE QUIERO PARA LOS NODOS
    try:
        while True:
            # Envia datos a los nodos en el grupo multicast
            print('Enviando {!r}'.format(message))
            sent = sock.sendto(message.encode('utf-8'), multicast_group)

            # Espera a recibir los "ack" de los nodos disponibles
            print('Esperando acks')
            lista = []
            lista_nodes = ["node1.actividad2_mcast-network","node2.actividad2_mcast-network","node3.actividad2_mcast-network"]

            while(True):
                try:
                    data, server = sock.recvfrom(4096)
                    alias = socket.gethostbyaddr(server[0]) #obtengo el nombre del host, ex: node1.network
                    hostip = socket.gethostbyname(alias[0]) #pruebo que efectivamente nodeX.network me de su ip
                    node_q.put(alias)
                    lista.append(alias[0])
                    

                    print('Recibidos {!r} desde {}'.format(data.decode('utf-8'), server))
                except:
                    print("Ningun otro nodo respondio con ACK")
                    break
            msg_q.put("Pulso Completo")
            heartbeat_server = open(r"/usr/src/app/server/heartbeat_server.txt","a")
            for i in lista:
                if i in lista_nodes:
                    lista_nodes.remove(i)
                heartbeat_server.write("Respondio: " + i + "\n")
            
            for j in lista_nodes:
                heartbeat_server.write("no respondio:"+j+" \n")
            heartbeat_server.close()
    finally:
        print('Cerrando socket')
        sock.close()

def Main():
    msg_q = Queue()
    node_q = Queue()
    not_resp_q = Queue()

    _thread.start_new_thread(thread_nodes, (msg_q, node_q,) )

    host = ""
    port = 5000
    print(socket.gethostbyname(socket.gethostname()))
    sock = socket.socket()
    sock.bind((host, port))
    print("Puerto asignado ", port)

    sock.listen(5)
    print("Socket Escuchando")

    while True:
        client, addrs = sock.accept()
        print("Conectado a: ", addrs[0], ":", addrs[1])
        _thread.start_new_thread(threaded, (client, msg_q, node_q, ) )
    sock.close()

if __name__ == '__main__':
    Main()