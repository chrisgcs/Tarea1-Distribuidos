import socket 
  
  
def Main(): 
    host = '127.0.0.1'
    port = 9889
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    sock.connect((host,port)) 
    message = "Hello i'm client"
    while True: 

        sock.send(message.encode('utf-8')) 
        data = sock.recv(1024) 
        print('Received from the server :', str(data.decode('utf-8'))) 
        ans = input('\nDo you want to continue(y/n) :') 
        if ans == 'y': 
            continue
        else: 
            break
    sock.close() 
  
if __name__ == '__main__': 
    Main() 