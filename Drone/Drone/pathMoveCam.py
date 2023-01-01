from djitellopy import Tello
import cv2
import sys
import time

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# file_name = sys.argv[1]
# f = open(file_name, "r")
# commands = f.readlines()

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()

while True:
    # In reality you want to display frames in a seperate thread. Otherwise
    # they will freeze while the drone moves.
    img = frame_read.frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow("drone", img)
    cv2.waitKey(1)

    key = cv2.waitKey(1) & 0xff
    if key == 27:  # ESC
        break
    elif key == ord('w'):
        tello.move_forward(30)
    elif key == ord('s'):
        tello.move_back(30)
    elif key == ord('a'):
        tello.move_left(30)
    elif key == ord('d'):
        tello.move_right(30)
    elif key == ord('e'):
        tello.rotate_clockwise(30)
    elif key == ord('q'):
        tello.rotate_counter_clockwise(30)
    elif key == ord('r'):
        tello.move_up(30)
    elif key == ord('f'):
        tello.move_down(30)

tello.land()