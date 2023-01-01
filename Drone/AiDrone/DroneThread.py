from djitellopy import tello
import cv2
import threading
from CurrentImg import Currentimg
from time import sleep
import KeyBoard


class DroneThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.curimg = Currentimg()
        self.drone = tello.Tello()
        self.drone.connect()
        self.drone.streamon()
        self.keyinputs = []
        KeyBoard.init()

    def getInput(self):
        left_right, front_back, up_down, clock_counter = 0, 0, 0, 0

        if KeyBoard.getKey("a"): left_right = -30
        if KeyBoard.getKey("d"): left_right = 30
        if KeyBoard.getKey("w"): front_back = 30
        if KeyBoard.getKey("s"): front_back = -30

        if KeyBoard.getKey("k"): up_down = 30
        if KeyBoard.getKey("l"): up_down = -30
        if KeyBoard.getKey("o"): clock_counter = -30
        if KeyBoard.getKey("p"): clock_counter = 30

        if KeyBoard.getKey("u"): self.drone.takeoff()
        if KeyBoard.getKey("h"): self.drone.land()

        self.keyinputs = [left_right, front_back, up_down, clock_counter]

    def run(self):
        img = self.drone.get_frame_read().frame
        img = cv2.resize(img, (640, 640))

        self.curimg.current_pimg = img
        self.curimg.current_oimg = img
        self.curimg.o_flag = True
        self.curimg.p_flag = True

        if (self.curimg.od_flag == True):
            img = self.curimg.current_oimg
            self.curimg.od_flag = False


        if (self.curimg.pd_flag == True):
            fullbody = self.curimg.body

            for (x, y, w, h) in fullbody:
                cv2.rectangle(img, (x, y), (x+w, y+h),(0, 255, 0), 3)

            self.curimg.pd_flag = False

        self.getInput()
        self.drone.send_rc_control(self.keyinputs[0], self.keyinputs[1], self.keyinputs[2], self.keyinputs[3])
        sleep(1)

        cv2.imshow("DroneView", img)
        cv2.waitKey(1)