import socket 
from datetime import datetime
import time
  
  
def Main():
    host = 'server'
    port = 5000
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    sock.connect((host,port)) 
    message = "Hello i'm client"
    mensajes = ["Mensaje 1", "Mensaje 2", "Mensaje 3", "Mensaje 4", "Mensaje 5", "Mensaje 6",
                "Mensaje 7", "Mensaje 8", "Mensaje 9", "Mensaje 10", "Mensaje 11", "Mensaje 12",
                "Mensaje 13", "Mensaje 14", "Mensaje 15", "Mensaje 16", "Mensaje 17", "Mensaje 18",
                "Mensaje 19", "Mensaje 20"]
    while True: 
        resp = open(r"/usr/src/app/cliente/respuestas.txt", "a")
        sock.send(message.encode('utf-8')) 
        data = sock.recv(1024)
        resp.write(data.decode('utf-8') + "\n")
        resp.close()
        print('Received from the server :',str(data.decode('utf-8'))) 
        for i in range(len(mensajes)):
            now = datetime.now()
            message = mensajes[i] + " " + str(now)
            sock.send(message.encode("utf-8"))
            time.sleep(0.2)
        message = "I`m leaving *drops mic*"
        sock.send(message.encode('utf-8'))
        resp = open(r"/usr/src/app/cliente/respuestas.txt", "a")
        data = sock.recv(1024)
        resp.write(data.decode('utf-8') + "\n")
        resp.close()
        break
    sock.close() 
  
if __name__ == '__main__': 
    Main() 