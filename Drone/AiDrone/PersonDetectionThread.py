import threading
import numpy as np
import cv2
from CurrentImg import Currentimg


class PersonDetectionThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.curimg = Currentimg()
        self.img = None
        self.grayimg = None
        self.fullbody_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_fullbody.xml')

    def run(self):
        if(self.curimg.p_flag == True):
            self.img = self.curimg.current_pimg
            self.grayimg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            fullbody = self.fullbody_cascade.detectMultiScale(self.grayimg, 1.01, 10)

            self.curimg.body = fullbody
            self.curimg.pd_flag = True
            self.curimg.p_flag = False



