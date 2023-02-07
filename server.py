import socket
import sys

HOST = '127.0.1'
PORT = 5789

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
'''
explaining this :
- socket.AF_IENT : socket type is internet socket 
- sock_stream : TCP port is used  
'''
try:
    soc.bind((HOST, PORT))
# bind is like making the script listen to that host on that port and wait for messages to be sent
except socket.error as message:

    print('Bind failed. Error Code : '
          + str(message[0]) + ' Message '
          + message[1])
    sys.exit()

print('Socket binding operation completed')
soc.listen(9)  # starts the server in listing mode and listen for 9 connections
while True:
    communication_socket, address = soc.accept()  # accept incoming requests

    ''' ^^ this is the communication socket that we can use later on to communicate with 
    that device on that address the socket that we created before is just for listening 
    to the port not for communication, its more of internal socket'''

    print(f'Connected with {address}')
    message = communication_socket.recv(1024).decode('utf-8')
    print(f'message is {message}')
    communication_socket.send(f"got your message {address}".encode('utf-8'))
