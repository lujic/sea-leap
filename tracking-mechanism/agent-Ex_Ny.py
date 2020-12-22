import os
import socket
import psycopg2

#name of the current Node host
HOST = "rll-m02"
#name of the edge site/cluster
EDGE_SITE = "E1"

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ensure that you can restart your server quickly when it terminates
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set the client socket's TCP "TCP_PORT" number
TCP_IP = ''
TCP_PORT = 5122
sock.bind((TCP_IP, TCP_PORT))

# Set the number of clients waiting for connection that can be queued
sock.listen(1)

# loop waiting for connections (terminate with Ctrl-C)
try:
    while 1:
        newSocket, address = sock.accept(  )
        print ("Connected from", address)
        # loop serving the new client
        while 1:
            receivedData = newSocket.recv(1024).decode()
            if not receivedData: break
            
            # Echo back the same data you just received
            newSocket.send(receivedData.encode())
            
            keys = receivedData.split()
            print(keys) 
            file_location = str(keys[0])
            file_name = str(keys[1])
            print(file_location)
            print(file_name)

            passw= "rucon2020"
            fetch = "sshpass -p " + passw + " scp -r " + file_location + ":/home/pi/datasets/" + file_name + " /data/samples"
            
            print (str(fetch))
            os.system(fetch)
            
            # update metadata
            con = psycopg2.connect(database="postgres", user="postgres", password="rucon2020", host="192.168.167.140", port="5432")
            print ("Database opened successfully")

            cur = con.cursor()

            userDataset = keys[1].split('.')[0]
            
            query = "UPDATE meta_db SET nodeLocation = '" + HOST + "' WHERE datasetID = '" + userDataset + "'";
            print (query)
            cur.execute(query)
            updated_rows = cur.rowcount
            con.commit()

            query = "UPDATE meta_db SET dataPath = '/data/samples/" + userDataset + "/' WHERE datasetID = '" + userDataset + "'";
            print (query)
            cur.execute(query)
            updated_rows = cur.rowcount
            con.commit()

            query = "SELECT * FROM meta_db";
            cur.execute(query)
            rows = cur.fetchall()
            
            print ("Database meta_db is updated!")
            for row in rows:
                print (row)

            con.close()

        newSocket.close(  )
        print ("Disconnected from", address)
finally:
    sock.close(  )


