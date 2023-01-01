import random
import socket
from time import sleep
import cv2
import threading
import numpy as np
from Code import Code
import torch

#
# 상태변환
# FILL_[ImageName] : 1 or 2 or 3
# 0. 안채움
# 1. 채우는중
# 2. 다채움

# 이미지 사이즈 전송
# SIZE_[ImageName] : 사이즈

# 이미지 데이터 받기
# RECV_[ImageName] : 데이터
#
# 연결
# CONN
#
class Server:
    __IP_Dict = dict()
    __picture_Dict = dict()
    __ServerIP = "172.17.32.131"
    __ServerPort = 9000
    __packetSize = 4096
    __codeSize = 128
    __sock: socket.socket

    def __init__(self):
        self.__sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # AF_INET -> IPv4 통신을 하겠다!! SOCK_DGRAM -> UDP 통신을 하겠다!!
        # AF_INET6 -> IPv6 통신을 하겠다!! SOCK_STREAM -> TCP 통신을 하겠다!!
        # 주소체계는 여러가지가 많지만 대표적으로 이거 두개정도만 알아두시면 될거같습니다!

        self.__sock.bind((self.__ServerIP, self.__ServerPort))

    def run(self):
        blank_model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best.pt', force_reload=True)
        recvthread = threading.Thread(target=self.recv)
        recvthread.start()

        cap = cv2.VideoCapture('test5.mp4')

        while cap.isOpened():
            ret, img = cap.read()

            if ret:
                blankresult = blank_model(img)
                df_blank = blankresult.pandas().xyxy[0]
                df_blank = df_blank[df_blank['confidence'] > 0.7]

                for i in range(len(df_blank)):
                    # print((df_blank.loc[i]['xmin'], df_blank.loc[i]['ymin']), (df_blank.loc[i]['xmax'], df_blank.loc[i]['ymax']))
                    cv2.rectangle(img, (int(df_blank.loc[i]['xmin']), int(df_blank.loc[i]['ymin'])),
                                  (int(df_blank.loc[i]['xmax']), int(df_blank.loc[i]['ymax'])), (0, 255, 0), 3)

                if blankresult is not None:
                    print("c 입력")
                    imageName = self.__createImageName()
                    self.__picture_Dict[imageName] = [img, 0]
                    sendImageThread = threading.Thread(target=self.__sendImage,
                                                       args=(imageName, self.__picture_Dict[imageName][0], None))
                    sendImageThread.start()

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def recv(self):
        print('recv 시작')

        while True:
            data, addr = self.__sock.recvfrom(1024)

            data = str(data, 'utf-8')

            if data == Code.CONN:
                print("CONN : ", addr)
                self.__IP_Dict[addr[0]] = addr[1]
                self.__sock.sendto(Code.CONN.encode(), (addr[0], addr[1]))
                connClientSendImageThread = threading.Thread(target=self.__connClientSendImage, args=(addr[0]))
                connClientSendImageThread.start()

            recvStr = data.split(" : ")

            if Code.STATE in recvStr[0]:
                imageName = recvStr[0].lstrip(Code.STATE)
                state = int(recvStr[1])

                if state != self.__picture_Dict[imageName][1]:
                    print(imageName, " : ", state)
                    self.__picture_Dict[imageName][1] = state
                    self.__send(self.__createCode(Code.STATE, imageName, state), addr[0])

    def __sendImage(self, imageName, frame, ip):
        retval, img_encode = cv2.imencode('.bmp', frame)
        data = img_encode.tostring()

        dataSize = len(data)
        sendSize = self.__packetSize - self.__codeSize
        count = 0
        lst = []

        while dataSize - count > 0:
            if dataSize < sendSize:
                imageSplitData = self.__getCode(Code.DATA, imageName).encode() + data[count: dataSize]
            else:
                imageSplitData = self.__getCode(Code.DATA, imageName).encode() + data[count: count + sendSize]

            lst.append(imageSplitData)
            count += sendSize

        self.__send(self.__createCode(Code.SIZE, imageName, len(lst)), None)

        for bytes in lst:
            if ip is None:
                self.__sendToAllClient(bytes, None)
            else:
                self.__send(bytes, ip)

            sleep(0.001)

        print(imageName, " 전송 완료")

    def __sendToAllClient(self, data, addr):
        for ip, port in self.__IP_Dict.items():
            if addr == ip:
                continue

        self.__sock.sendto(data, (ip, port))

    def __send(self, data, ip):
        port = self.__IP_Dict[ip]
        self.__sock.sendto(data, (ip, port))

    def __connClientSendImage(self, ip):
        sleep(2)
        for imageName in self.__picture_Dict.keys():
            sendImageThread = threading.Thread(target=self.__sendImage,
                                               args=(imageName, self.__picture_Dict[imageName][0], ip))
            sendImageThread.start()

    def __getCode(self, action: str, imageName: str):
        return action + imageName + " : "

    def __createCode(self, action: str, imageName: str, code):
        if type(code) != str:
            code = str(code)

        sendData = action + imageName + " : " + code

        return sendData.encode()

    def __createImageName(self):
        chars = "abcdefghijklmnopqrstuvwsyz123456789"

        name = ""
        for i in range(8):
            name += random.choice(chars)

        return name



