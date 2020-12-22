import time
import pandas as pd
import numpy as np

class nodeSpec:
    def __init__(self, nodeType, avgInference):
        self.nodeType = nodeType
        self.avgInference = avgInference
 
class networkSpec:
    def __init__(self, networkType, avgLatency, avgBandwidth):
        self.networkType = networkType
        self.avgLatency = avgLatency
        self.avgBandwidth = avgBandwidth

class candidateSpec:
    def __init__(self, nodeName, edgeSite, nodeType, totalLatency, edgeCluster, nodeIP, nodeIPsrc):
        self.nodeName = nodeName
        self.edgeSite = edgeSite
        self.nodeType = nodeType
        self.totalLatency = totalLatency
        self.edgeCluster = edgeCluster
        self.nodeIP = nodeIP
        self.nodeIPsrc = nodeIPsrc

class initNodesSpec:
    def __init__(self, nodeName, edgeCluster):
        self.nodeName = nodeName
        self.edgeCluster = edgeCluster

class newNodesSpec:
    def __init__(self, nodeName, edgeSite, nodeType, edgeCluster, nodeIP):
        self.nodeName = nodeName
        self.edgeSite = edgeSite
        self.nodeType = nodeType
        self.edgeCluster = edgeCluster
        self.nodeIP = nodeIP


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
networkBenchmarks = list()
nodeBenchmarks = list()
initCandidates = list()
newCandidates = list()
index = None

# appending instances to lists
# interence latency benchmarks in the Knowledge base
nodeBenchmarks.append( nodeSpec('A', '0.01781') )
nodeBenchmarks.append( nodeSpec('B', '0.25074') )
nodeBenchmarks.append( nodeSpec('C', '0.50062') )


#networkBenchmarks.append( networkSpec('3G', '0.24792', '19.02') )
#networkBenchmarks.append( networkSpec('4G', '0.02344', '48.11') )
#networkBenchmarks.append( networkSpec('5G', '0.01383', '116') )

#alternative location candidates retrieved from the Knowledge base
newCandidates.append( newNodesSpec('rll-h01', 'E2', 'C', 'rll-haydn', '192.168.167.101') )
newCandidates.append( newNodesSpec('rll-b01', 'E3', 'C', 'rll-beethoven', '192.168.167.171') )
newCandidates.append( newNodesSpec('intrabox01', 'E4', 'B', 'rll-intrabox01', '192.168.167.150') )
newCandidates.append( newNodesSpec('intrabox02', 'E5', 'A', 'rll-intrabox02', '192.168.167.160') )

# node dictionary stored in the Knowledge base; can be extended with new edge nodes
nodeDict =[
        ['rll-m01', 'E1', 'C', '192.168.167.121'], 
        ['rll-m02', 'E1', 'C', '192.168.167.122'],  
        ['rll-m03', 'E1', 'C', '192.168.167.123'],
        ['rll-mozart', 'E1', 'C', '192.168.167.120'],
        ['rll-h01', 'E2', 'C', '192.168.167.101'],
        ['rll-h02', 'E2', 'C', '192.168.167.102'],
        ['rll-h03', 'E2', 'C', '192.168.167.103'],
        ['rll-haydn', 'E2', 'C', '192.168.167.100'],
        ['rll-b01', 'E3', 'C', '192.168.167.171'],
        ['rll-beethoven', 'E3', 'C', '192.168.167.170'],
        ['intrabox01', 'E4', 'B', '192.168.167.150'],
        ['intrabox02', 'E5', 'A', '192.168.167.160']
        ]  

# network details stored in the Knowledge base; can be extended for  each edge site 
networkDict = [
        ['3G', '0.24792', '8.81'],
        ['4G', '0.02344', '41.43'],
        ['5G', '0.01383', '66.55']
        ]

# creating df object with columns specified     
#nodes_df = pd.DataFrame(nodeDict, columns =['nodeName', 'edgeSite', 'nodeType'])  

#------------------------------------

#datasetMetadata = ['cam-intra-09072020d1', '91.4', '600'] 
#datasetMetadata = ['cam-pennfudan-09072020d2', '25.2', '60']
#datasetMetadata = ['cam-sher-09072020d3', '154', '1800']
#datasetMetadata = ['cam-rene-09072020d4', '1011.8', '3600']


#for node in nodeDict:
 #print(node[0])
#print (datasetLocations[2].location)
#if (datasetLocations[0].datasetID == userDataset)
#for obj in networkHops['E1']:
#    print (obj)
#for obj in locationCandidates:
    #if (obj.datasetID ==  userDataset):
        #index = datasetLocations.index(obj)
#    print (obj.nodeName)
    
#print (locationCandidates[0].nodeName)

#r = 4
#t = testing.jointversion(r)
#print (t)

def placementCalculation(meta):
    datasetMetadata = meta
    
    # initial location candidates considering dataset location
    #initCandidates.append( initNodesSpec('rll-m01', 'rll-mozart') )
    initCandidates.append( initNodesSpec(datasetMetadata[3],datasetMetadata[4]))
    for node_init in initCandidates: 
        #retrieve corresponding edgeSite and nodeType of initial nodes
        for node in nodeDict:
            if (node[0] == node_init.nodeName):
                edgeSiteInit = node[1]
                nodeType = node[2]
                nodeIPsrc = node[3]
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
        locationCandidates.append( candidateSpec(node_init.nodeName, edgeSiteInit, nodeType, T_R, node_init.edgeCluster, nodeIPsrc, nodeIPsrc) )
    
        for node_new in newCandidates:
            if (node_new.nodeName != node_init.nodeName):
                edgeSiteNew = node_new.edgeSite
                nodeType = node_new.nodeType
                nodeIP = node_new.nodeIP
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
                locationCandidates.append(candidateSpec(node_new.nodeName, edgeSiteNew, nodeType, TL, node_new.edgeCluster, nodeIP, nodeIPsrc))


    L_ap.append(locationCandidates[0])
    #print(L_ap[0].totalLatency)
    #print("Location candidates are the following:")
    for cand in locationCandidates:
        #print (cand.nodeName, cand.edgeSite, cand.nodeType, cand.totalLatency)
        if (cand.totalLatency < L_ap[0].totalLatency):
            L_ap[0] = cand

    #print ("\nThe most appropriate node location is " + str(L_ap[0].nodeName) + " from cluster " + str(L_ap[0].edgeSite) + " with minimum estimated latency of " + str(L_ap[0].totalLatency) + "s")
    return (L_ap)
