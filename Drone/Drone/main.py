import Server
from djitellopy import Tello
import cv2
from threading import Thread
import time
import torch

print('Load Model ...')
blank_model = torch.load('./weights/best_blank.pt')
person_model = torch.load('./weight/best_person.pt')

print('Load Path ...')
file_name = 'command.txt'
f = open(file_name, "r")
commands = f.readlines()

# print('Init App Server ...')
# server = Server.Server()
# server.run()

print('Init Tello Drone ...')
tello = Tello()
tello.connect()
tello.streamon()
frame_read = tello.get_frame_read()

print('Tello Take Off')
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
        pass

# Drone Driving Thread Start
dronemove = Thread(target=droneMove)
dronemove.start()

while True:
    img = frame_read.frame

    personresult = person_model(img)
    df_person = personresult.pandas().xyxy[0]
    df_person = df_person[df_person['name'] == 'person']
    df_person = df_person[df_person['confidence'] > 0.8]
    if df_person is not None:
        # DETECT_PERSON = True
        for i in range(len(df_person)):
            # print((df_person.iloc[i]['xmin'], df_person.iloc[i]['ymin']), (df_person.iloc[i]['xmax'], df_person.iloc[i]['ymax']))
            cv2.rectangle(img, (int(df_person.iloc[i]['xmin']), int(df_person.iloc[i]['ymin'])),
                          (int(df_person.iloc[i]['xmax']), int(df_person.iloc[i]['ymax'])), (255, 0, 0), 3)
            cv2.putText(img, df_person.iloc[i]['name'],
                        (int(df_person.iloc[i]['xmin']), int(df_person.iloc[i]['ymin'] - 6)), cv2.FONT_ITALIC, 1,
                        (255, 0, 0), 2)

    cv2.imshow("Drone View", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
tello.land()
dronemove.join()