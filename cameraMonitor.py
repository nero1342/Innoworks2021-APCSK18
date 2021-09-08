from Models.datahub import DataHub
from Models.Transportation.model import Model 

import requests
import base64
import cv2
import random 
import json 
import os
import time 
import datetime 
import csv

class CameraMonitor:
    def __init__(self, transportation_model_path):
        self.numCam = 2
        self.listFrames = [sorted(os.listdir(f'static/Cam_{i}')) for i in range(self.numCam)]
        self.frameId = [random.randint(0, len(self.listFrames[i]) - 1) for i in range(self.numCam)]
        
        self.transportation = ['bus', 'car', 'motorbike', 'truck']
        self.objectList = self.transportation + ['number of people']

        configs = { 
            # 'Activity Level': ['Activity Level'],
            'Camera 1': self.transportation + ['Activity Level'],
            'Camera 2': self.transportation + ['Activity Level'],
        }

        self.datahub = DataHub(configs)

        self.transportation_model = Model(pretrained_path=transportation_model_path)

    def run(self):
        bef = [random.randint(10, 20) for i in range(self.numCam)]

        while True:
            for i in range(self.numCam):
                # Prepare image from camera
                self.frameId[i] = (self.frameId[i] + 1) % len(self.listFrames[i])
                frame = self.listFrames[i][self.frameId[i]] 

                # Save last image to visualize in dashboard 
                os.system(f'cp static/Cam_{i}/{frame} static/last_{i}.jpeg')

                # Run model
                response = self.transportation_model.forward(os.path.abspath(f'static/Cam_{i}/{frame}'))

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

                time.sleep(1)

cameraMonitor = CameraMonitor(transportation_model_path = 'Models/Transportation/model_final.pth')
cameraMonitor.run()