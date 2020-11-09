# Lint as: python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example using TFLite to detect objects in a given image datasets."""

from PIL import Image
from PIL import ImageDraw
import os
import detect
import tflite_runtime.interpreter as tflite
import platform
import datetime
import cv2
import time
import numpy as np
import io
from io import BytesIO
from flask import Flask, request, Response, jsonify
import random
import re

EDGETPU_SHARED_LIB = {
  'Linux': 'libedgetpu.so.1',
  'Darwin': 'libedgetpu.1.dylib',
  'Windows': 'edgetpu.dll'
}[platform.system()]

confThreshold = 0.5

app = Flask(__name__)

def load_labels(path, encoding='utf-8'):
  """Loads labels from file (with or without index numbers).

  Args:
    path: path to label file.
    encoding: label file encoding.
  Returns:
    Dictionary mapping indices to labels.
  """
  with open(path, 'r', encoding=encoding) as f:
    lines = f.readlines()
    if not lines:
      return {}

    if lines[0].split(' ', maxsplit=1)[0].isdigit():
      pairs = [line.split(' ', maxsplit=1) for line in lines]
      return {int(index): label.strip() for index, label in pairs}
    else:
      return {index: line.strip() for index, line in enumerate(lines)}


def make_interpreter(model_file):
  model_file, *device = model_file.split('@')
  return tflite.Interpreter(
      model_path=model_file,
      experimental_delegates=[
          tflite.load_delegate(EDGETPU_SHARED_LIB,
                               {'device': device[0]} if device else {})
      ])

def draw_objects(draw, objs, labels):
  """Draws the bounding box and label for each object."""
  for obj in objs:
    bbox = obj.bbox
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    color=tuple(rgbl)
    draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],
                   outline=color)
    draw.text((bbox.xmin + 10, bbox.ymin + 10),
              '%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score),
              fill=color)

def detection_loop(filename_image, path, output):
  labels = load_labels(labelsPath) if labelsPath else {}
  interpreter = make_interpreter(modelPath)
  interpreter.allocate_tensors()
  summ = 0 
  
  #check if folder results exists, otherwise make it and make it accessible
  if (os.path.isdir(path+'results') == False):
      #print("The output folder " + output + " does not exist! It will be created")
      os.system("mkdir " + path + "results")
      #os.system("sudo chmod 777 ./results")
  #make output.txt for results of the inference and make it accessible
  os.system("touch "+ path + "results/output.txt")
  #os.system("sudo chmod 777 ./results/output.txt")

  for filename, image in filename_image.items():
      #image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
      #image = Image.fromarray(image)
      scale = detect.set_input(interpreter, image.size, lambda size: image.resize(size, Image.ANTIALIAS))
      for _ in range(1):
          
          start = time.perf_counter()
          #run inference by invoking the Interpreter
          interpreter.invoke()
          #calculate inference time 
          inference_time = time.perf_counter() - start
          
          #get the output data
          objs = detect.get_output(interpreter,confThreshold,scale)
          
          print('\n\nIT TOOK %f ms' % (inference_time * 1000) + " on image " + filename + "\n")
          summ=summ+(inference_time * 1000)
          #os.chmod("./results/output.txt", 0o777)
          with open (path+"results/output.txt", "a") as f:
              f.write(
                      "%f \n" % (inference_time * 1000)
                      )
          print ('--------RESULTS--------')
          if not objs:
              #with open (path+"results/output.txt", "a") as f:
               #   f.write("No objects detected"
                #          )
              print('No objects detected')
          for obj in objs:
              #with open (path+"results/output.txt", "a") as f:
               #   f.write(
                #          labels.get(obj.id, obj.id) + 
                 #         "\n  score: %s\n--\n" % obj.score
                  #        )
              print(labels.get(obj.id, obj.id))
              #print('  id:    ', obj.id)
              print('  score: ', obj.score)
              #print('  bbox:  ', obj.bbox)
          
          if output != None:
              image = image.convert('RGB')
              draw_objects(ImageDraw.Draw(image), objs, labels)
              #image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
              #np_img = Image.fromarray(image)
              #byte_io = BytesIO()
              #os.system("sudo chmod 777 ./results") 
              #spliting filename from extension
              split_filename = filename.split(".", 1)
              image.save(path+"results/"+split_filename[0]+"-annnotated.png", format='PNG')

  print ('%.7f' % (summ / 100))

labelsPath = "models/coco_labels.txt"
modelPath = "models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"

#initializing the flask app
app = Flask(__name__)

#routing http posts to this method
@app.route('/api/detect', methods=['POST', 'GET'])
def main():
  #img = request.files["image"].read()
  #image = Image.open(io.BytesIO(img))
  #data_input = request.args['input']
  data_input = request.values.get('input')
  output = request.values.get('output')
  #output = request.form.get('output')

  path = data_input
  filename_image = {}
  
  input_format = ["jpg", "png", "jpeg"]
  if data_input.find(".") != -1:
      print(data_input + " is a file")
      split_data_input = data_input.split(".", 1)
      if data_input.endswith(tuple(input_format)):
          print("INPUT FORMAT: %s IS VALID" % split_data_input[1])
          path_splitted = []
          path_splitted = re.split('/', data_input)
          filename = path_splitted[len(path_splitted)-1]
          filename_image[filename] = Image.open(data_input)
          path = os.path.dirname(data_input)+"/"
  else:
      print(data_input + " is a path with the following files: ")
      for filename in os.listdir(data_input):
          image_path = data_input + filename
          filename_image[filename] = Image.open(image_path)
          print("  " + filename)
  
  detection_loop(filename_image, path, output)
  
  status_code = Response(status = 200)
  return status_code
# image=cv2.imread(args.input)
# image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
