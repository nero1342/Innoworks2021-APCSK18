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
import shutil

from utils.image import encode_image
from utils.config import Config 
import yaml 

from heatmap import heatmap2png, genRelatedPoints, heatmap2html
from notification import Notification 

# random.seed(12345678)

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

        print("Datahub connecting...")
        self.datahub = DataHub(datahub_configs)

        # Camera's location
        pts = [(10.762913,106.6821717), (10.765913,106.6524717), (10.7739789,106.6880888), (10.7735451,106.6637059),
                (10.7586745,106.6317317), (10.744487,106.6390273), (10.7643547,106.66642), (10.7338196,106.6511723),
                (10.7986166,106.6576985), (10.8164056,106.6637925),
                (10.7752692,106.6929486),
        ]

        self.related_pts = [genRelatedPoints(pt) for pt in pts]

        print("Init notification...")
        self.notification = Notification(cfg) 
        noti_auth_response = self.notification.auth()
        print("Notifictaion auth: ", noti_auth_response.text) 

    def url(self, port):
        return f'{self.cfg.ADDRESS}:{port}/predict'

    def run(self):
        print("Camera Monitor Starting..")
        bef = [random.randint(10, 20) for i in range(self.numCam)]

        last_time_noti = [None for i in range(self.numCam)]

        while True:
            try:
                for i in range(self.numCam):
                    print("Query camera ", i)
                    # Prepare image from camera
                    self.frameId[i] = (self.frameId[i] + 1) % len(self.listFrames[i])
                    frame = self.listFrames[i][self.frameId[i]] 

                    # Save last image to visualize in dashboard 
                    shutil.copy2(f'data/Cam_{i}/{frame}', f'services/static/last_{i}.jpeg') 
                    
                    # Run model
                    response_transportation = json.loads(requests.post(self.url(self.cfg.TRANSPORTATION.PORT), json = {'image': encode_image(os.path.abspath(f'data/Cam_{i}/{frame}'))}).text)
                    response_pedestron = json.loads(requests.post(self.url(self.cfg.PEDESTRON.PORT), json = {'image': encode_image(os.path.abspath(f'data/Cam_{i}/{frame}'))}).text)
                    
                    response = {**response_transportation, **response_pedestron}
                    
                    activityLevel = 0
                    for tag in response:
                        if tag in self.objectList: activityLevel += int(response[tag])

                    bef[i] = activityLevel

                    # Send data to Datahub
                    self.datahub.sendData(f'Camera {i + 1}', 'Activity Level', activityLevel)
                    for x in self.transportation:
                        if x in response:
                            self.datahub.sendData(f'Camera {i + 1}', x, int(response[x]))

                    # Notification

                    if last_time_noti[i] is not None:
                        print(f"Wait {self.cfg.NOTIFICATION.INTERVAL - (time.time() - last_time_noti[i])} seconds for the next notification")
                    if (activityLevel >= self.cfg.NOTIFICATION.THRESHOLD) and \
                        ((last_time_noti[i] is None) or ((time.time() - last_time_noti[i]) >= self.cfg.NOTIFICATION.INTERVAL)):
                        last_time_noti[i] = time.time() 
                        self.notification.sendMessage()

                        print("Sent from camera ", i)
                    print(response)
                    fields=[datetime.datetime.now(), activityLevel]
                    print(f"Time: {fields[0]} - At frame frame {self.frameId[i]} - {frame} - activityLevel: {activityLevel}")


                if self.cfg.CAMERA_MONITOR.USE_HEATMAP:
                    locations = [(pt, bef[i % self.numCam] * 2) for i, pt in enumerate(self.related_pts)]
                    heatmap2png("services/static/heatmap.png", locations)
                    # print(locations)
                    # heatmap2html("out.html", locations)
                    
                time.sleep(self.cfg.CAMERA_MONITOR.SLEEP_TIME)

            except Exception as e: 
                print(e)
                pass 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.yaml', help='Configuration')
    args = parser.parse_args()
    service_cfg = Config(yaml.load(open(args.config, 'r'), Loader=yaml.Loader))

    cameraMonitor = CameraMonitor(service_cfg)
    cameraMonitor.run()