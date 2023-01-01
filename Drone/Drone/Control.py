from djitellopy import tello
from time import sleep
import cv2
import KeyBoard
import torch

def getInput():
    left_right, front_back, up_down, clock_counter = 0, 0, 0, 0

    if KeyBoard.getKey("a"): left_right = -30
    if KeyBoard.getKey("d"): left_right = 30
    if KeyBoard.getKey("w"): front_back = 30
    if KeyBoard.getKey("s"): front_back = -30

    if KeyBoard.getKey("k"): up_down = 30
    if KeyBoard.getKey("l"): up_down = -30
    if KeyBoard.getKey("o"): clock_counter = -30
    if KeyBoard.getKey("p"): clock_counter = 30

    if KeyBoard.getKey("u"): drone.takeoff()
    if KeyBoard.getKey("h"): drone.land()

    return [left_right, front_back, up_down, clock_counter]

def videoStream():
    img = drone.get_frame_read().frame
    return img
if __name__ == '__main__':
    drone = tello.Tello()
    drone.connect()
    KeyBoard.init()
    drone.streamon()

    while True:
        img = videoStream()

        cv2.imshow("Drone View", img)
        cv2.waitKey(1)

        keyinputs = getInput()
        drone.send_rc_control(keyinputs[0], keyinputs[1], keyinputs[2], keyinputs[3])
        sleep(1)


