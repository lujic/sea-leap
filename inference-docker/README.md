## inference-docker - steps
*(Deployment of object detection app is inspired by the following post https://medium.com/analytics-vidhya/object-detection-using-yolo-v3-and-deploying-it-on-docker-and-minikube-c1192e81ae7a)*

1. Build docker image from Dockerfile
~~~
#with tpu
docker build -t inference-at-arm32v7-slim-buster:edgetpu-v2 .

#without tpu
docker build -t inference-at-arm32v7-slim-buster:notpu-v2 .
~~~
2a. Run docker container locally
~~~
#docker image with tpu (allowing to access tpu)
docker run -d -p 5000:5000 --privileged -v /dev/bus/usb:/dev/bus/usb inference-at-arm32v7-slim-buster:edgetpu-v2

#docker image without tpu
docker run -d -p 5000:5000 inference-at-arm32v7-slim-buster:notpu-v2
~~~
* Test inference
~~~
#run inference on single image files from a path
curl http://localhost:5000/api/detect -d "input=/data/samples/06.jpg"
#run inference on multiple image files from a folder path
curl http://localhost:5000/api/detect -d "input=/data/samples/"
#to save annotated images, add a "flag" by adding any character to "output"
curl http://localhost:5000/api/detect -d "input=/data/samples/06.jpg&output=1"
curl http://localhost:5000/api/detect -d "input=/data/samples/&output=1"
~~~
2b. Deploy inference on Kubernetes
~~~
#pay attention to a specified docker image and other details in the manifest file inference.yaml
kubectl apply -f inference.yaml

#test inference by submiting image(s) path from "outside". We can pass data path in cURL by using -d. Considering the manifest file,
# hostPath as a Volume is used to mount a specific folder from the host), enabling inference to access image dataset from the passed values (input)
kubectl exec inference-notpu -- curl http://localhost:5000/api/detect -d "input=/data/samples/" 

#access container in a pod
kubectl exec --stdin --tty inference-notpu -- /bin/bash
~~~
3. The output data, i.e., the .txt file with detected objects and scores as well as (if requested) annotated images, can be find in the same folder (whose path is specified as the input)
