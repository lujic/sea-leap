import time
import pandas as pd
import numpy as np

class nodeSpec:
    def __init__(self, nodeType, avgInference):
        self.nodeType = nodeType
        self.avgInference = avgInference
 
class candidateSpec:
    def __init__(self, nodeName, edgeSite, nodeType, totalLatency):
        self.nodeName = nodeName
        self.edgeSite = edgeSite
        self.nodeType = nodeType
        self.totalLatency = totalLatency

class initNodesSpec:
    def __init__(self, nodeName, master):
        self.nodeName = nodeName
        self.master = master

class newNodesSpec:
    def __init__(self, nodeName, edgeSite, nodeType):
        self.nodeName = nodeName
        self.edgeSite = edgeSite
        self.nodeType = nodeType


column_names = ['E1', 'E2', 'E3', 'E4', 'E5']
row_names = ['E1', 'E2', 'E3', 'E4', 'E5']
#network topology, static number of hops between edge sites, stored in the Knowledge base 
matrix = np.reshape((
    0,1,2,2,3,
    1,0,1,1,2,
    2,1,0,1,1,
    2,1,1,0,1,
    3,2,1,1,0),
    (5,5))

#create matrix forming number of hops between different edge sites  
networkHops = pd.DataFrame(matrix, columns=column_names, index=row_names)

# get value from (column,row)
#print(H['E1']['E5'])

# creating lists
locationCandidates = list()
L_ap = list()
nodeBenchmarks = list()
initCandidates = list()
newCandidates = list()
index = None

# appending instances to lists
# interence latency benchmarks in the Knowledge base
nodeBenchmarks.append( nodeSpec('A', '0.01781') )
nodeBenchmarks.append( nodeSpec('B', '0.25074') )
nodeBenchmarks.append( nodeSpec('C', '0.50062') )

# initial location candidates considering dataset location
initCandidates.append( initNodesSpec('rll-m01', 'rll-mozart') )

#alternative location candidates retrieved from the Knowledge base
newCandidates.append( newNodesSpec('rll-h01', 'E2', 'C') )
newCandidates.append( newNodesSpec('rll-b01', 'E3', 'C') )
newCandidates.append( newNodesSpec('rll-intrabox01', 'E4', 'B') )
newCandidates.append( newNodesSpec('rll-intrabox02', 'E5', 'A') )

#node dictionary stored in the Knowledge base; can be extended with new edge nodes
nodeDict =[
        ['rll-m01', 'E1', 'C'], 
        ['rll-m02', 'E1', 'C'],  
        ['rll-m03', 'E1', 'C'],
        ['rll-mozart', 'E1', 'C'],
        ['rll-h01', 'E2', 'C'],
        ['rll-h02', 'E2', 'C'],
        ['rll-h03', 'E2', 'C'],
        ['rll-haydn', 'E2', 'C'],
        ['rll-b01', 'E3', 'C'],
        ['rll-beethoven', 'E3', 'C'],
        ['rll-intrabox01', 'E4', 'B'],
        ['rll-intrabox02', 'E5', 'A']
        ]  

#network details stored in the Knowledge base (KB); can be extended for  each edge site 
networkDict = [
        ['3G', '0.24792', '8.81'],
        ['4G', '0.02344', '41.43'],
        ['5G', '0.01383', '66.55']
        ]

#------------------------------------

datasetMetadata = ['cam-intra-09072020d1', '91.4', '600'] 
#datasetMetadata = ['cam-pennfudan-09072020d2', '25.2', '60']
#datasetMetadata = ['cam-sher-09072020d3', '154', '1800']
#datasetMetadata = ['cam-rene-09072020d4', '1011.8', '3600']


for node_init in initCandidates: 
    #retrieve corresponding edgeSite and nodeType of initial nodes
    for node in nodeDict:
        if (node[0] == node_init.nodeName):
            edgeSiteInit = node[1]
            nodeType = node[2]
    #retrieve inference time for specific node type
    for bench in nodeBenchmarks:
        if (bench.nodeType == nodeType):
            inf_time = bench.avgInference
    #retrieve number of frames from forwarded dataset information
    no_frames = datasetMetadata[2]
    #print(inf_time)
    #print(no_frames)
    #calculate total runtime for for executing request
    T_R = round((float(inf_time)*float(no_frames)), 5)
    
    #add initial location candidate
    locationCandidates.append( candidateSpec(node_init.nodeName, edgeSiteInit, nodeType, T_R) )
    
    for node_new in newCandidates:
        if (node_new.nodeName != node_init.nodeName):
            edgeSiteNew = node_new.edgeSite
            nodeType = node_new.nodeType
            #print(edgeSiteNew)
            #print(nodeType)

            for bench in nodeBenchmarks:
                if (bench.nodeType == nodeType):
                    inf_time = bench.avgInference
            
            no_frames = datasetMetadata[2]
            #print(inf_time)
            #print(no_frames)
            T_R = round(float(inf_time)*float(no_frames), 5)

            no_hops = networkHops[edgeSiteInit][edgeSiteNew]
            #print(no_hops)
            size_d = float(datasetMetadata[1])
            #latency and bandwidth can be checked for different benchmarked configurations (first element): 0->3G, 1->4G, 2->5G 
            lat = float(networkDict[2][1])
            bw = float(networkDict[2][2]) / 8
            T_MV = round((lat + no_hops * (size_d/bw)), 5)
            #print(size_d)
            #print(lat)
            #print(bw)
            TL = T_R + T_MV
            locationCandidates.append(candidateSpec(node_new.nodeName, edgeSiteNew, nodeType, TL))


L_ap.append(locationCandidates[0])
#print(L_ap[0].totalLatency)
print("Location candidates to run inference on dataset " + str(datasetMetadata[0]) + " are the following:")
print("-------------")
for cand in locationCandidates:
    print (cand.nodeName, cand.edgeSite, cand.nodeType, cand.totalLatency)
    if (cand.totalLatency < L_ap[0].totalLatency):
        L_ap[0] = cand
print("-------------")
print ("\nThe most appropriate node location is " + str(L_ap[0].nodeName) + " from cluster " + str(L_ap[0].edgeSite) + " with minimum estimated latency of " + str(L_ap[0].totalLatency) + "s")
