import socket
import os
import time
import yaml
import psycopg2
import pandas as pd

#class datasetSpec:
#    def __init__(self, datasetID, location, cluster):
#        self.datasetID = datasetID
#        self.location = location
#        self.cluster = cluster

# creating list,datasetLocations=list()
#datasetLocations = list()

# initializing index that will point to the corresponding dataset in the database
#index = None

# appending instances to list
#datasetLocations.append( datasetSpec('cam-e1-0907202010', 'rll-m01', 'rll-mozart') )
#datasetLocations.append( datasetSpec('cam-e3-0907202010', 'rll-h02', 'rll-haydn') )
#datasetLocations.append( datasetSpec('cam-e2-0907202011', 'rll-m03', 'rll-mozart') )

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ensure that you can restart your server quickly when it terminates
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set the client socket's TCP "TCP_PORT" number
TCP_IP = ''
TCP_PORT = 5001
sock.bind((TCP_IP, TCP_PORT))

# Set the number of clients waiting for connection that can be queued
sock.listen(3)

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

            # separate submitted message into separate strings stored in an array
            keys = receivedData.split()
             
            # first key is user-specified datasetID
            userDataset = keys[0]
            #print (userDataset)
            #for obj in datasetLocations:
            #    if (obj.datasetID ==  userDataset):
            #        index = datasetLocations.index(obj)
            
            # open connection to postgresql database
            con = psycopg2.connect(database="postgres", user="postgres", password="", host="127.0.0.1", port="5432")
            print("Database opened successfully")
            
            cur = con.cursor()
            query = "SELECT * FROM meta_db WHERE datasetID LIKE '" + userDataset + "'";
            cur.execute(query)
            metadata = cur.fetchall()
            con.close()
            
            # proceed only if required  dataset ID exists in the database
            if metadata:

                # convert fetched data to dataframe
                col_names = []
                for elt in cur.description:
                    col_names.append(elt[0])
                df = pd.DataFrame(metadata, columns = col_names)

                print ( "Dataset " + df["datasetid"][0] + " located in node " + df["nodelocation"][0] + " within the cluster " + df["clusterlocation"][0] )
                
                # open yaml template
                with open("template-inference-notpu.yaml", 'r') as stream:
                    try:
                        data = yaml.safe_load(stream)
                        #print(data)
                    except yaml.YAMLError as exc:
                        print(exc)

                # inject missing dataset location to spec.nodeName
                data["spec"]["nodeName"] = df["nodelocation"][0]

                #print (data['spec']['nodeName'])
                
                # save dict to mutated yaml file, ready for deployment
                with open('test.yaml', 'w+') as outfile:
                    yaml.dump(data, outfile, default_flow_style=False)
                
                #for key, value in data["spec"].items():
                    #print (key, value)
                
                context = "kubectl config use-context " + df["clusterlocation"][0]
                print (context)
                os.system(context)
                os.system('kubectl config get-contexts')
                os.system('kubectl apply -f test.yaml')
                #time.sleep(3)
                os.system('kubectl get pods -o wide')
                os.system('kubectl config use-context rll-meta')
                os.system('kubectl config get-contexts')
            else: 
                print ("The submitted datasetID " + userDataset + " does not exist in the database!")
        newSocket.close(  )
        print ("Disconnected from", address)
finally:
    sock.close(  )
