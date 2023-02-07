import socket

HOST = '127.0.1'
PORT = 5789
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))
while True:
    socket.send(input("enter your message ").encode('utf-8'))
    print(socket.recv(1024))
