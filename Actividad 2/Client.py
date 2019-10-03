import socket 
from datetime import datetime
import time
  
  
def Main():
    host = 'headnode.actividad2_client-server'
    port = 5000
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    sock.connect((host,port)) 
    message = "Hola, soy un cliente"
    mensajes = ["Mensaje 1", "Mensaje 2", "Mensaje 3", "Mensaje 4", "Mensaje 5", "Mensaje 6",
                "Mensaje 7", "Mensaje 8", "Mensaje 9", "Mensaje 10", "Mensaje 11", "Mensaje 12",
                "Mensaje 13", "Mensaje 14", "Mensaje 15", "Mensaje 16", "Mensaje 17", "Mensaje 18",
                "Mensaje 19", "Mensaje 20"]
    while True: 
        sock.send(message.encode('utf-8')) 
        data = sock.recv(1024)

        print('Recibido desde el servidor :',str(data.decode('utf-8'))) 
        flag = True
        while flag :
            aviso = sock.recv(1024)
            if aviso.decode("utf-8") == "send messages":
                flag = False
            else:
                time.sleep(1)
        for i in range(len(mensajes)):
            now = datetime.now()
            message = mensajes[i] + " " + str(now)
            print("Enviando " + mensajes[i])
            sock.send(message.encode("utf-8"))
            
            donde = sock.recv(1024).decode("utf-8")
            if donde == "send messages":
                donde = sock.recv(1024).decode("utf-8")
            registro_cliente = open(r"/usr/src/app/cliente/registro_cliente.txt","a")
            registro_cliente.write(donde)
            registro_cliente.close()

            time.sleep(5)
        
        message = "Adios"
        sock.send(message.encode('utf-8'))
        data = sock.recv(1024)
        if data == "send messages":
            data = sock.recv(1024)
        break
    sock.close() 
  
if __name__ == '__main__': 
    Main() 