import os
import cv2
import torch
import numpy as np 
from models.Pedestron.mmdet.apis import inference_detector, init_detector, show_result

class PedestronModel:
    def __init__(self, cfg):
        print("Init Pedestron model...")
        self.model = init_detector(
            cfg.PEDESTRON.CONFIG, cfg.PEDESTRON.weight, device=torch.device('cuda:0'))

    def forward(self, image, is_path = True):
        if is_path:
            image = cv2.imread(image)
            
        print("forwarding...")
        results = inference_detector(self.model, image)

        if isinstance(results, tuple):
            bbox_result, segm_result = results
        else:
            bbox_result, segm_result = results, None

        bboxes = np.vstack(bbox_result)
        score_thr = 0.3
        if score_thr > 0:
            assert bboxes.shape[1] == 5
            scores = bboxes[:, -1]
            inds = scores > score_thr
            bboxes = bboxes[inds, :]
            # labels = labels[inds]

        return {"pedestron": bboxes.shape[0]}

if __name__ == "__main__":
    model = PedestronModel()
    img = cv2.imread('/home/nero/Innoworks2021-APCSK18/services/last_1.jpeg')
    x = model.forward(img, is_path = False)
    print(x)