#!/usr/bin/env python

import socket


TCP_IP = '192.168.167.122'
TCP_PORT = 5122
BUFFER_SIZE = 1024
MESSAGE = "pi@192.168.167.121 cam-pennfudan-31Dec20"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode())
data = s.recv(BUFFER_SIZE)
s.close()

print(data.decode())
