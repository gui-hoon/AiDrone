import threading
import random
import socket
from time import sleep
import cv2
import numpy as np
from enum import Enum
from CurrentImg import Currentimg

class State(Enum):
    NOT_FILL = 1
    FILLING = 2
    FINISH = 3

class Code:
    DATA = "DATA_"
    SIZE = "SIZE_"
    STATE = "FILL_"
    CONN = "CONN"


class Server:

    def __init__(self):
        threading.Thread.__init__(self)
        self.curimg = Currentimg()
        self.__IP_Dict = dict()
        self.__picture_Dict = dict()
        self.__ServerIP = "192.168.35.145"
        self.__ServerPort = 9000
        self.__packetSize = 4096
        self.__codeSize = 128
        self.__sock: socket.socket

        self.__sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.__sock.bind((self.__ServerIP, self.__ServerPort))

    def recv(self):
        print('recv 시작')

        while True:
            data, addr = self.__sock.recvfrom(1024)

            data = str(data, 'utf-8')

            if data == Code.CONN:
                print("CONN : ", addr)
                self.__IP_Dict[addr[0]] = addr[1]
                self.__sock.sendto(Code.CONN.encode(), (addr[0], addr[1]))

            recvStr = data.split(" : ")

            if Code.STATE in recvStr[0]:
                imageName = recvStr[0].lstrip(Code.STATE)
                state = int(recvStr[1])

                if state != self.__picture_Dict[imageName][1]:
                    print(imageName, " : ", state)
                    self.__picture_Dict[imageName][1] = state
                    self.__sendCode(Code.STATE, imageName, state, addr[0])

    def sendImage(self, frame):
        imageName = self.__createImageName()
        self.__picture_Dict[imageName] = [frame, 0]

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

        self.__sendCode(Code.SIZE, imageName, len(lst), None)

        for i, bytes in enumerate(lst):
            self.__send(bytes, None)
            sleep(0.001)

        print(imageName, " 전송 완료")


    def __send(self, data, addr):
        for ip, port in self.__IP_Dict.items():
            if addr == ip:
                continue

            self.__sock.sendto(data, (ip, port))

    def __sendCode(self, action: str, imageName: str, code, addr):
        if type(code) != str:
            code = str(code)

        sendData = action + imageName + " : " + code
        self.__send(sendData.encode(), addr)

    def __getCode(self, action: str, imageName: str):
        return action + imageName + " : "

    def __createImageName(self):
        chars = "abcdefghijklmnopqrstuvwsyz123456789"

        name = ""
        for i in range(8):
            name += random.choice(chars)

        return name

    def Start(self):
        self.recvthread = threading.Thread(target=self.recv)
        self.recvthread.start()





