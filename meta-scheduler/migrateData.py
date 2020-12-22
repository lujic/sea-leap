#!/usr/bin/env python

import socket

def migrate(host_ip, src_ip, datasetid):

    #TCP_IP = '192.168.167.160'
    TCP_IP = host_ip
    TCP_PORT = 5122
    BUFFER_SIZE = 1024
    MESSAGE = "pi@"+str(src_ip)+ " " + str(datasetid)
    #print(MESSAGE)
    #print(TCP_IP)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE.encode())
    data = s.recv(BUFFER_SIZE)
    s.close()
    
    print("Target data moved from " + str(src_ip) + " to " + str(host_ip))
    #print(data.decode())
