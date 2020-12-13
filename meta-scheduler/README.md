## Steps for running meta scheduler with other SEA-LEAP services

* testing meta scheduler with only guideMe action (i.e., run analytics request at the node location storing requested dataset)
~~~~
#run meta-sched-guideme-only.py on "meta server"
python3 meta-sched-guideme-only.py

#send request from any other client/node location by adapting and running tcp-client.py
python3 tcp-client.py

#observe results by checking running status of the deployed Kubernetes pod and output file with detected objects on /data/<datasetname>/results/ path (on target node)
~~~~
