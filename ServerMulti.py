import socket
import threading
import _thread

print_lock = threading.Lock()

def threaded(client):
    while(True):
        data = client.recv(1024).decode('utf-8')
        if (not data or data == 'exit'):
            print("Fuck it, i'm out")
            print_lock.release()
            break
        print(data)
        out = "Hello i'm server"
        client.send(out.encode('utf-8'))
    client.close()

def Main():
    host = ""
    port = 9889
    sock = socket.socket()
    sock.bind((host, port))
    print("Binded to port ", port)

    sock.listen(5)
    print("Socket Listening")

    while (True):
        client, addrs = sock.accept()
        print_lock.acquire()
        print("Connected to: ", addrs[0], ":", addrs[1])

        _thread.start_new_thread(threaded, (client,))
    sock.close()

if __name__ == '__main__':
    Main()