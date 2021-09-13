from models.datahub import DataHub
# from Models.Transportation.model import Model 

import argparse

import requests
import cv2
import random 
import json 
import os
import time 
import datetime 
import csv

from utils.image import encode_image
from utils.config import Config 
import yaml 

class CameraMonitor:
    def __init__(self, cfg):

        self.cfg = cfg

        self.numCam = 2
        self.listFrames = [sorted(os.listdir(f'data/Cam_{i}')) for i in range(self.numCam)]
        self.frameId = [random.randint(0, len(self.listFrames[i]) - 1) for i in range(self.numCam)]
        
        self.transportation = ['bus', 'car', 'motorbike', 'truck']
        self.objectList = self.transportation + ['pedestron']

        datahub_configs = { 
            # 'Activity Level': ['Activity Level'],
            'Camera 1': self.transportation + ['Activity Level'],
            'Camera 2': self.transportation + ['Activity Level'],
        }

        self.datahub = DataHub(datahub_configs)

    def url(self, port):
        return f'{self.cfg.ADDRESS}:{port}/predict'

    def run(self):
        bef = [random.randint(10, 20) for i in range(self.numCam)]

        while True:
            try:
                for i in range(self.numCam):
                    # Prepare image from camera
                    self.frameId[i] = (self.frameId[i] + 1) % len(self.listFrames[i])
                    frame = self.listFrames[i][self.frameId[i]] 

                    # Save last image to visualize in dashboard 
                    os.system(f'cp data/Cam_{i}/{frame} services/static/last_{i}.jpeg')

                    # Run model
                    # response = self.transportation_model.forward(os.path.abspath(f'static/Cam_{i}/{frame}'))
                    response_transportation = json.loads(requests.post(self.url(self.cfg.TRANSPORTATION.PORT), json = {'image': encode_image(os.path.abspath(f'data/Cam_{i}/{frame}'))}).text)
                    response_pedestron = json.loads(requests.post(self.url(self.cfg.PEDESTRON.PORT), json = {'image': encode_image(os.path.abspath(f'data/Cam_{i}/{frame}'))}).text)
                    
                    response = {**response_transportation, **response_pedestron}
                    # Calculate activity level
                    for tag in self.objectList:
                        if tag not in response.keys():
                            # Pedestron is not working now -> random instead
                            response[tag] = random.randint(max(10, bef[i] - 1), min(30, bef[i] + 1))
                            bef[i] = response[tag]

                    activityLevel = 0
                    for tag in response:
                        if tag in self.objectList: activityLevel += int(response[tag])

                    # Send data to Datahub
                    self.datahub.sendData(f'Camera {i + 1}', 'Activity Level', activityLevel)
                    for x in self.transportation:
                        if x in response:
                            self.datahub.sendData(f'Camera {i + 1}', x, int(response[x]))

                    print(response)
                    fields=[datetime.datetime.now(), activityLevel]
                    print(f"Time: {fields[0]} - At frame frame {self.frameId[i]} - {frame} - activityLevel: {activityLevel}")

                    time.sleep(self.cfg.CAMERA_MONITOR.SLEEP_TIME)
            except:
                pass 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.yaml', help='Configuration')
    args = parser.parse_args()
    service_cfg = Config(yaml.load(open(args.config, 'r'), Loader=yaml.Loader))

    cameraMonitor = CameraMonitor(service_cfg)
    cameraMonitor.run()