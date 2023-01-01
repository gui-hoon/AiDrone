from djitellopy import Tello
import cv2
from threading import Thread
import time
import torch

print('Load Model ...')
blank_model = torch.load('./weights/best_blank.pt')
person_model = torch.load('./weights/best_person.pt')

print('Load Path ...')
file_name = 'command.txt'
f = open(file_name, "r")
commands = f.readlines()

print('Init Tello Drone ...')
tello = Tello()
tello.connect()
tello.streamon()
frame_read = tello.get_frame_read()

print('Tello Take Off')
tello.takeoff()

DRONESTART = False
DETECT_PERSON = False


def droneRecord(img):
    r_time = str(time.time()) + '.png'
    save_path = './capture/'
    cv2.imwrite(save_path+r_time, img)


def droneMove():
    # global capture_flag
    global DETECT_PERSON
    IS_UP = False
    prev_command = ''
    index = 0

    while index < len(commands):
        if DETECT_PERSON is not True:
            if IS_UP is True:
                tello.send_control_command("down 80")
                IS_UP = False

            command = commands[index]
            print(command)
            index += 1
            if command != '' and command != '\n':
                command = command.rstrip()
                if command.find('delay') != -1:
                    sec = float(command.partition('delay')[2])
                    print('delay %s' % sec)
                    time.sleep(sec)
                    pass
                else:
                    if command.find('cw') != -1:
                        if prev_command.find('ccw') != -1:
                            print('capture')
                            recordTh = Thread(target=droneRecord, args=(frame_read.frame, ))
                            recordTh.start()

                    tello.send_control_command(command)
                    # capture_flag = False
                    # print(f'cur command: {command}\tprv commane: {prev_command}')
                    prev_command = command

        else:
            if IS_UP is False:
                tello.send_control_command("up 80")
                IS_UP = True


# Drone Driving Thread Start
dronemove = Thread(target=droneMove)
dronemove.start()

while True:
    img = frame_read.frame
    personresult = person_model(img)
    df_person = personresult.pandas().xyxy[0]
    df_person = df_person[df_person['name'] == 'person']
    df_person = df_person[df_person['confidence'] > 0.8]

    if len(df_person) > 0:
        DETECT_PERSON = True
        for i in range(len(df_person)):
            cv2.rectangle(img, (int(df_person.iloc[i]['xmin']), int(df_person.iloc[i]['ymin'])),
                          (int(df_person.iloc[i]['xmax']), int(df_person.iloc[i]['ymax'])), (255, 0, 0), 3)
            cv2.putText(img, df_person.iloc[i]['name'],
                        (int(df_person.iloc[i]['xmin']), int(df_person.iloc[i]['ymin'] - 6)), cv2.FONT_ITALIC, 1,
                        (255, 0, 0), 2)

    elif len(df_person) == 0:
        DETECT_PERSON = False


    cv2.imshow("Drone View", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
print('Drone land')
tello.land()
dronemove.join()