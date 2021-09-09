# check pytorch installation: 
import torch, torchvision
print(torch.__version__, torch.cuda.is_available())
# assert torch.__version__.startswith("1.9")   # please manually install torch 1.9 if Colab changes its default version

# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg

class TransportationModel:
    def __init__(self, pretrained_path):
        pass
        print("Constructing model...")
        cfg = get_cfg()
        # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
        cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
        # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
        cfg.MODEL.WEIGHTS = pretrained_path
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4    
        self.predictor = DefaultPredictor(cfg)
        self.name = ['motorbike', 'car', 'truck', 'bus']
        
    def forward(self, im, is_path = True):
        if is_path:
            im = cv2.imread(im)
            
        print("forwarding...")
        outputs = self.predictor(im)
        from collections import Counter 
        result = Counter(outputs["instances"].pred_classes.tolist())
        # print(outputs)
        out = {}
        for i in range(len(self.name)):
            if i not in result.keys():
                out.update({self.name[i]: 0})
            else:
                out.update({self.name[i]: result[i]})
        # print(result[0], result[1], result[2], result[3])
        return out

if __name__ == "__main__":
    model = Model(pretrained_path='/vinai/rone/AIoT/model_final.pth')
    img = cv2.imread('/vinai/rone/AIoT/WISEPaaS.DataHub.Edge.Python.SDK.Sample/static/last_0.jpeg')
    x = model.forward(img, is_path = False)
    print(x)