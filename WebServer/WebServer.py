import os
import sys
import time
import socket
import threading
from socket import AF_INET, SOCK_STREAM


def handle_request(connection_socket):
    try:
        message = connection_socket.recv(1024).decode()
        if not message:
            return
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        modified_time = os.path.getmtime(filename[1:])
        # Send one HTTP header line into socket
        if 'If-Modified-Since' not in message or (
                'If-Modified-Since' not in message and message.split(
                    'If-Modified-Since: ', 1)[1].strip()) < modified_time:
            # If there is no If-Modified-Since request or file was not changed
            connection_socket.send('HTTP/1.1 200 OK\r\n\
            \rConnection: close\r\n\
            \rDate: {}\r\n\
            \rLast-Modified: {}\r\n\
            \rContent-Type: text/html\r\n\r\n'.format(
                time.ctime(), time.ctime(modified_time)).encode())
            # Send the content of the requested file to the client
            connection_socket.sendall(outputdata.encode())
            connection_socket.send('\r\n'.encode())
        else:
            connection_socket.send('HTTP/1.1 304 Not Modified\r\n\
            \rContent-Type: text/html\r\n\r\n'.encode())

        connection_socket.close()
    except IOError:
        # Send response message for file not found
        connection_socket.send('HTTP/1.1 404 Not Found\r\n\
        \rContent-Type: text/html\r\n\r\n'.encode())
        connection_socket.send(
            '<html><body><h1>Sorry, there is no such file!</h1>\
            <h2>Please visit home.html</h2></body></html>'.encode())
        # Close client socket
        connection_socket.close()


if __name__ == '__main__':
    server_socket = socket.socket(AF_INET, SOCK_STREAM)
    # Prepare a sever socket
    server_socket.bind(('', 62666))
    server_socket.listen(1)
    while True:
        # Establish the connection
        print(socket.gethostname() + ' Ready to serve...')
        connection_socket, addr = server_socket.accept()
        t = threading.Thread(target=handle_request, args=(connection_socket, ))
        print('{} is visiting by {}...'.format(addr, t.getName()))
        t.start()
    server_socket.close()
    sys.exit()  # Terminate the program after sending the corresponding data
