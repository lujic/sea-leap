# SEA-LEAP
SEA-LEAP is a framework for Self-adaptive and Locality-aware Edge Analytics Placement. It includes: 

1\. an agent-based mechanism for tracking data movements, on top of which a generic control mechanism is devised, featuring: 

2a. a meta-scheduler allowing a guided deployment of on-demand analytics applications to node locations storing required input datasets,

2b. a placement service enabling on-demand analytics placement to the most appropriate dataset location based on adaptive data movements that minimizes overall analytics requests execution time.

The current SEA-LEAP is developed in Python (requiring additional packages such as pandas, numpy, socket, psycopg2) and uses Kubernetes platform for the experimental evaluation. 

*******************************************************************
This repository includes the following elements/services:

- **inference-benchmark** - aims to obtain inference latency benchmarks for different (RPi) node types. 
- **inference-docker** - contains source files to build docker images for the object detection logic. 
- **placementServiceSimulation.py** - simulates the calculation of the most appropriate location for a set of configurable information: dataset, edge node specifications, analytics, network topology and characteristics. 
- **tracking-mechnaism** - aims to build agent monitoring services and metadata-database for registration and tracking of data movements. 
- **meta-scheduler** - aims to self-adaptively guide the placement of requested analytics processing based on data locality. 

*******************************************************************

## TESTBED
The simulation-based evaluation is based on a physical edge infrastructure consisted of Raspberry Pi (RPi) single-board computers available in different configurations (RPi 3 B+, RPi 4, with and without edge TPU - Coral USB accelerator).

## DATA
The proposed algorithms are evaluated on different real-world datasets (typically used in computer vision analytics applications such as object detection), namely:
* InTraSafEd 5G project (https://newsroom.magenta.at/2020/01/16/5g-anwendungen-in-wien/) for increasing traffic safety with Edge and 5G, obtained during the project evaluation. The datasets contain sampled video frames in various sizes from the chosen Vienna’s intersection used for the real-time detection of critical situations
and to support drivers in avoiding accidents (due to objects that can appear in drivers’ blind spots).
* Dataset Penn-Fudan comes from an image database used for object detection and recognition on scenes around campuses and urban streets [1]. Selected frames represent various angles and image qualities of captured objects such as pedestrians, bikes and cars.
* Datasets Sherbrooke and Rene-Levesque come from the cameras monitoring different intersections, used for detecting and tracking multiple objects of various types in outdoor
urban traffic surveillance [2].

## APPLICATION use case
The analytics application runs a quantized version of SSD MobileNet v2 model, a lightweight and pre-trained convolutional neural network (CNN) based object detection. The object detection logic is dockerized, and (after starting) exposed (using Flask) as a service running in a container (that can be accessed using API (http://localhost:5000/api/detect). Corresponding docker images are publicly available on the Docker hub repository (https://hub.docker.com/r/ilujic/inference-arm32v7/).

## ACKNOWLEDGMENTS 
This work has been partially funded through the Rucon project (Runtime Control in Multi Clouds), FWF Y 904 START-Programm 2015, 5G Use Case Challenge InTraSafEd 5G (Increasing Traffic Safety with Edge and 5G) funded by the City of Vienna and supported through Ivan Lujic’s netidee scholarship by the Internet Foundation Austria.

## REFERENCES 
[1] L. Wang, J. Shi, G. Song, and I.-F. Shen, “Object detection combining recognition and segmentation,” in Asian conference on computer vision. Springer, 2007, pp. 189–199.

[2] J.-P. Jodoin, G.-A. Bilodeau, and N. Saunier, “Urban tracker: Multiple object tracking in urban mixed traffic,” in IEEE Winter Conference on Applications of Computer Vision. IEEE, 2014, pp. 885–892.
