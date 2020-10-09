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

confThreshold = 0.4

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
  return tflite.Interpreter(model_path=model_file)

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

def detection_loop(image):
  labels = load_labels(labelsPath) if labelsPath else {}
  interpreter = make_interpreter(modelPath)
  interpreter.allocate_tensors()

  success = 1
  while success:
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
          
          print('%.5f ms' % (inference_time * 1000))
#          summ=summ+(inference_time * 1000)
          with open ("speed.txt", "a") as f:
              f.write("%.5f\n" % (inference_time * 1000))
          print('-------RESULTS--------')
          if not objs:
              print('No objects detected')
          for obj in objs:
              print(labels.get(obj.id, obj.id))
              print('  id:    ', obj.id)
              print('  score: ', obj.score)
              print('  bbox:  ', obj.bbox)
          
          if success:
              image = image.convert('RGB')
              draw_objects(ImageDraw.Draw(image), objs, labels)
              #image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
              #np_img = Image.fromarray(image)
              #byte_io = BytesIO()
              image.save("results/image-annotated.png", format='PNG')

      success = 0
#  print (summ / 100)

labelsPath = "models/coco_labels.txt"
modelPath = "models/mobilenet_ssd_v2_coco_quant_postprocess.tflite"

#initializing the flask app
app = Flask(__name__)

#routeing http posts to this method
@app.route('/api/detect', methods=['POST'])
def main():
  img = request.files["image"].read()
  image = Image.open(io.BytesIO(img))
#  npimg = np.array(img)
#  image = npimg.copy()
#  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  detection_loop(image)
  
  status_code = Response(status = 200)
  return status_code
# image=cv2.imread(args.input)
# image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
