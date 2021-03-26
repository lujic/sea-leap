## Steps for running meta scheduler with other SEA-LEAP services

* test meta scheduler with only guideMe action (i.e., run analytics request at the node location storing requested dataset)
~~~~
#run meta-sched-guideme-only.py on "meta server"
python3 meta-sched-guideme-only.py

#send request from any other client/node location by adapting and running tcp-client.py
python3 tcp-client2.py

#observe results by checking running status of the deployed Kubernetes pod and output file with detected objects on /data/<datasetname>/results/ path (on target node)
~~~~
* complete meta-scheduler workflow with both guideMe and followMe actions (i.e., runing analytics at the most appropriate node location by considering both the data localiy and minimizing overall estimated analytics request execution time)
~~~~
#run agents on available nodes by adapting to corresponding topology and testbed, for example, running agent-intrabox02.py on "intrabox02" node
python3 agent-intrabox02.py

#run meta-scheduler on meta-server, i.e., the main node (including meta-dataset db, Knowledge base, placement service) able to communicate with all available nodes
python3 meta-sched-complete.py

#send request from any other client/node location by adapting and running tcp-client.py
python3 tcp-client.py

#observe results by checking output of the target node agent, updated database entries, running status of the deployed Kubernetes pod, and output file with detected objects on /data/<datasetname>/results/ path (on target node)
~~~~
