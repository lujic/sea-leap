#!/usr/bin/env python

import socket


TCP_IP = '192.168.167.140'
TCP_PORT = 5001
BUFFER_SIZE = 1024
MESSAGE = "cam-intrasafed-31Dec20 inference-v1"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode())
data = s.recv(BUFFER_SIZE)
s.close()

print (data.decode())
