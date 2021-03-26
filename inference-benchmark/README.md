## Obtaining average inference latency for edge nodes (RPi 3 B+, RPi 4 with or without TPU)

* run object detection application
~~~
python3 app.py
~~~
* run *curl* from another session specifying a folder path that contains a set of image files
~~~
curl http://localhost:5000/api/detect -d "input=/data/samples/" 
~~~
* obtain results of average inference per image frame for target edge node type 
