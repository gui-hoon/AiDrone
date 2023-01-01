from djitellopy import Tello
import cv2
from threading import Thread
import sys, time

file_name = 'command.txt'
f = open(file_name, "r")
commands = f.readlines()



tello = Tello()
tello.connect()
tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()

DETECT_PERSON = False

def droneMove():
    if DETECT_PERSON is not True:
        for command in commands:
            if command != '' and command != '\n':
                command = command.rstrip()

                if command.find('delay') != -1:
                    sec = float(command.partition('delay')[2])
                    print('delay %s' % sec)
                    time.sleep(sec)
                    pass
                else:
                    tello.send_command_without_return(command)
    else:
        tello.send_command_without_return('up 50')

dronemove = Thread(target=droneMove)
dronemove.start()

while True:
    img = frame_read.frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow("drone", img)
    cv2.waitKey(1)

