import socket
import threading
import _thread

print_lock = threading.Lock()

def threaded(client):
    out = "Hello i'm server"
    client.send(out.encode('utf-8'))
    while(True):
        file = open("log.txt", "a")
        data = client.recv(1024).decode('utf-8')
        file.write(data+"\n")
        if (data == "I`m leaving *drops mic*"):
            #print("Ok thank you have a nice day")
            out = "Ok thank you have a nice day"
            client.send(out.encode('utf-8'))
            #print_lock.release()
            break
        print(data)
        file.close()
    client.close()

def Main():
    host = ""
    port = 5000
    sock = socket.socket()
    sock.bind((host, port))
    print("Binded to port ", port)

    sock.listen(5)
    print("Socket Listening")

    while (True):
        client, addrs = sock.accept()
        #print_lock.acquire()
        print("Connected to: ", addrs[0], ":", addrs[1])

        _thread.start_new_thread(threaded, (client,))
    sock.close()

if __name__ == '__main__':
    Main()