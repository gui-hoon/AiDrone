from djitellopy import tello
from time import sleep
import cv2
from KeyBoard import KeyBoard
import threading

class DroneControl:
    def __init__(self):
        self.drone = tello.Tello()
        self.drone.connect()
        self.keyboard = KeyBoard()
        self.keyboard.init()
        self.drone.streamon()

        self.imgFlag = False
        self.img = None
        self.blankFlag = False
        self.personFlag = False

    def setImgFlag(self):
        self.imgFlag = True

    def getImgFlag(self):
        return self.imgFlag

    def setPersonFlag(self):
        self.personFlag = True

    def getPersonFlag(self):
        return self.personFlag

    def setBlankFlag(self):
        self.blankFlag = True

    def getBlankFlag(self):
        return self.blankFlag

    def getInput(self):
        left_right, front_back, up_down, clock_counter = 0, 0, 0, 0

        if self.keyboard.getKey("a"): left_right = -30
        if self.keyboard.getKey("d"): left_right = 30
        if self.keyboard.getKey("w"): front_back = 30
        if self.keyboard.getKey("s"): front_back = -30

        if self.keyboard.getKey("k"): up_down = 30
        if self.keyboard.getKey("l"): up_down = -30
        if self.keyboard.getKey("o"): clock_counter = -30
        if self.keyboard.getKey("p"): clock_counter = 30

        if self.keyboard.getKey("u"): self.drone.takeoff()
        if self.keyboard.getKey("h"): self.drone.land()

        return [left_right, front_back, up_down, clock_counter]


    def run(self):
        while True:
            # if self.getPersonFlag() == True:
            #     print("detect person")
            self.img = self.drone.get_frame_read().frame
            # self.img = cv2.rotate(self.img, cv2.ROTATE_180)
            # self.setImgFlag()
            cv2.imshow("Drone View", self.img)
            cv2.waitKey(1)
            # keyinputs = self.getInput()
            # self.drone.send_rc_control(keyinputs[0], keyinputs[1], keyinputs[2], keyinputs[3])
            # sleep(1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
