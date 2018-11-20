# UDPPingerClient.py
import numpy
import socket
import time
from socket import AF_INET, SOCK_DGRAM

# Create a TCP socket
# Notice the use of SOCK_DGRAM for UDP packets
socket.setdefaulttimeout(1)
client_socket = socket.socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
server_name = 'localhost'
server_port = 12000
loss, rtts = 0, []
# send 10 message
for i in range(1, 11):
    message = f'Ping {str(i)} {str(time.time()):<018}'
    # start recording time
    rtt = time.time()
    client_socket.sendto(message.encode(), (server_name, server_port))
    try:
        message, address = client_socket.recvfrom(1024)
        # response received
        rtts.append((time.time() - rtt) * 1000)
        print(
            f'{message.decode()} from {address} by RTT {rtts[-1]:<05.3}ms'
        )
    except socket.timeout:
        print('Request timed out')
        loss += 1
print('-'*70)
print(f'Max RTT: {max(rtts):<05.3}ms')
print(f'Min RTT: {min(rtts):<05.3}ms')
print(f'Average RTT: {numpy.mean(rtts):<05.3}ms')
print(f'Packet loss : {loss / 10:%<05.2%}')