FROM arm32v7/python:3.7.9-slim-buster
MAINTAINER Rucon@TUW "ivan@ec.tuwien.ac.at"

RUN apt-get update -y && apt-get install -y --no-install-recommends curl python3-pip python3-dev libsm6 libxext6 libxrender-dev libatlas-base-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libopencv-dev build-essential pkg-config libjpeg-dev libpng-dev libgtk-3-dev && rm -rf /var/lib/apt/lists/*

#Allow pi wheels 
RUN echo "[global]\nextra-index-url=https://www.piwheels.org/simple" >> /etc/pip.conf

#Copy the requirements.txt to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

# Upgrade pip and install requirements
RUN pip3 install --upgrade pip; pip3 install --no-cache-dir -r requirements.txt; pip3 install --no-cache-dir https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
