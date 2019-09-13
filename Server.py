import socket

port = 5000
sock = socket.socket()
print("Success!!!!")

sock.bind(('', port))
print("socket binded to ", port)

sock.listen(5)
print("Listening")

while(True):
    client, adress = sock.accept()
    print("Got connection from ", adress)
    out = "Thanks Fucker"
    client.send(out.encode('utf-8'))
    client.close()