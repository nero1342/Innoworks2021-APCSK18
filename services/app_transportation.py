import sys
sys.path.append('.')
sys.path.append('..')

import argparse

import numpy as np 
import os
from flask import Flask, request, jsonify 
from PIL import Image 
import cv2 
import io   
from base64 import decodestring

# Model
from models.transportation import TransportationModel
import torch

from utils.config import Config 
import yaml 

app = Flask(__name__)

@app.route('/predict', methods = ['POST'])
def predict():
    encoded_image = request.get_json(force = True)['image']
    with open('services/static/image.png', 'wb') as f:
        f.write(decodestring(encoded_image.encode('utf-8')))

    return jsonify(transportation_model.forward('services/static/image.png'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.yaml', help='Configuration')
    args = parser.parse_args()
    config = Config(yaml.load(open(args.config, 'r'), Loader=yaml.Loader))

    transportation_model = TransportationModel(config.TRANSPORTATION.WEIGHT)

    port = int(os.environ.get('PORT', config.TRANSPORTATION.PORT))
    app.run(port = port, debug = True, use_reloader = False)

