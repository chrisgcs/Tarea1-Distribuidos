import socket 
from datetime import datetime
import time
  
  
def Main():
    host = 'headnode'
    port = 5000
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    sock.connect((host,port)) 
    message = "Hello i'm client"
    mensajes = ["I'm still", "standing", "yeah", "yeah", "yeah"]
    while True: 
        sock.send(message.encode('utf-8')) 
        data = sock.recv(1024)

        print('Received from the server :',str(data.decode('utf-8'))) 
        flag = True
        while flag :
            aviso = sock.recv(1024)
            if aviso.decode("utf-8") == "send messages":
                flag = False
            else:
                time.sleep(6)
        for i in range(5):
            now = datetime.now()
            message = mensajes[i] + " " + str(now)
            sock.send(message.encode("utf-8"))
            
            donde = sock.recv(1024).decode("utf-8")
            if donde == "send messages":
                donde = sock.recv(1024).decode("utf-8")
            print(donde)
            registro_cliente = open("registro_cliente.txt","a")
            registro_cliente.write(donde)
            registro_cliente.close()

            time.sleep(5)
        
        message = "I`m leaving *drops mic*"
        sock.send(message.encode('utf-8'))
        data = sock.recv(1024)
        if data == "send messages":
            data = sock.recv(1024)
        print(data)
        break
    sock.close() 
  
if __name__ == '__main__': 
    Main() 