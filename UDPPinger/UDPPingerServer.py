# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import time
import random
import socket
from socket import AF_INET, SOCK_DGRAM

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', 12000))
seq = 0
while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    diff = time.time() - float(message.decode().split()[2])
    # Check the sequence number
    if int(message.decode().split()[1]) != seq + 1:
        if int(message.decode().split()[1]) == 1:
            seq = 0
        else:
            print(f'Packet {seq + 1} lost!')
            seq += 1
            continue
    # Capitalize the message from the client
    message = message.upper()
    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
        seq += 1
        continue
    # Otherwise, the server responds
    serverSocket.sendto(message, address)
    # Set sequemce number
    seq += 1
