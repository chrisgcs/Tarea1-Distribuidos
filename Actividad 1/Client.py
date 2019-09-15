import socket 
  
  
def Main(): 
    host = '127.0.0.1'
    port = 5000
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    sock.connect((host,port)) 
    message = "Hello i'm client"
    while True: 
        resp = open("respuestas.txt", "a")
        sock.send(message.encode('utf-8')) 
        data = sock.recv(1024)
        resp.write(data.decode('utf-8') + "\n")
        resp.close()
        print('Received from the server :',str(data.decode('utf-8'))) 
        ans = input('\nDo you want to continue(y/n) :') 
        if ans == 'y': 
            continue
        else:
            message = "I`m leaving *drops mic*"
            sock.send(message.encode('utf-8'))
            resp = open("respuestas.txt", "a")
            data = sock.recv(1024)
            resp.write(data.decode('utf-8') + "\n")
            resp.close()
            break
    sock.close() 
  
if __name__ == '__main__': 
    Main() 