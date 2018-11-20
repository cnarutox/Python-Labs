import socket
import sys
from socket import AF_INET, SOCK_STREAM

host, port, filename = sys.argv[1:]
client_socket = socket.socket(AF_INET, SOCK_STREAM)
client_socket.connect((host, int(port)))
client_socket.send('GET /{} HTTP/1.1'.format(filename).encode())
client_socket.send('Host: {}'.format(host).encode())
client_socket.send('Connection: close'.encode())
print(client_socket.recv(2048).decode(), client_socket.recv(9999).decode())