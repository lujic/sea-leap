## inference-docker - steps for building docker images
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
