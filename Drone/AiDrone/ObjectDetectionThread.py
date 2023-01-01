import threading
from CurrentImg import Currentimg
import time
import cv2
import torch
import torch.backends.cudnn as cudnn
import numpy as np

from numpy import random
from models.experimental import attempt_load
from utils.augmentations import letterbox
from utils.general import check_img_size, check_requirements, non_max_suppression, scale_coords
from utils.plots import Annotator
from utils.torch_utils import select_device

class ObjectDetectionThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.curimg = Currentimg()
        self.WEIGHTS = './weights/best.pt'
        self.IMG_SIZE = 640
        self.DEVICE = ''
        self.AUGMENT = False
        self.CONF_THRES = 0.25
        self.IOU_THRES = 0.45
        self.CLASSES = None
        self.AGNOSTIC_NMS = False
        #self.server = Server

    def run(self):
        if (self.curimg.o_flag == True):
            source, weights, imgsz = self.curimg.current_oimg, self.WEIGHTS, self.IMG_SIZE

            # Initialize
            device = select_device(self.DEVICE)
            half = device.type != 'cpu'  # half precision only supported on CUDA
            print('device:', device)

            # Load model
            model = attempt_load(weights, map_location=device)  # load FP32 model
            stride = int(model.stride.max())  # model stride
            imgsz = check_img_size(imgsz, s=stride)  # check img_size
            if half:
                model.half()  # to FP16

            # Get names and colors
            names = model.module.names if hasattr(model, 'module') else model.names
            colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

            # Run inference
            if device.type != 'cpu':
                model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once

            # Load image
            img0 = cv2.imread(source)  # BGR
            assert img0 is not None, 'Image Not Found ' + source

            # Padded resize
            img = letterbox(img0, imgsz, stride=stride)[0]

            # Convert
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
            print(img.shape, img0.shape)
            img = np.ascontiguousarray(img)

            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            pred = model(img, augment=self.AUGMENT)[0]
            print('pred shape:', pred.shape)

            # Apply NMS
            pred = non_max_suppression(pred, self.CONF_THRES, self.IOU_THRES, classes=self.CLASSES, agnostic=self.AGNOSTIC_NMS)

            # Process detections
            det = pred[0]
            print('det shape:', det.shape)

            s = ''
            s += '%gx%g ' % img.shape[2:]  # print string

            if len(det):
                # Rescale boxes from img_size to img0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    annotator = Annotator(img0, line_width=3, example=str(names))
                    c = int(cls)  # integer class
                    label = f'{names[int(cls)]} {conf:.2f}'
                    #plot_one_box(xyxy, img0, label=label, color=colors[int(cls)], line_thickness=3)
                    annotator.box_label(xyxy, label, color=colors(c, True))

            self.curimg.current_oimg = img0
            #self.server.sendImage(img0)
            self.curimg.od_flag = True
            self.curimg.o_flag = False