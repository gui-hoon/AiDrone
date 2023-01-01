import random
import socket
from time import sleep
import threading
from Code import Code
import cv2

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
    __ServerIP = "192.168.10.2"
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
        recvthread = threading.Thread(target=self.recv)
        recvthread.start()

        # cap = cv2.VideoCapture(0)
        # img = cv2.imread('test.png')
        # img = cv2.resize(img, (960, 640))
        #
        # while cap.isOpened() :
        #     ret, frame = cap.read()
        #
        #     if not ret :
        #         break
        #
        #     cv2.imshow('test', frame)
        #
        #     if cv2.waitKey(1) == ord('q'):
        #         break

        #    if cv2.waitKey(1) == ord('c'):
        #         print("c 입력")
        #         splitImageNames = ""
        #         for key in self.__IP_Dict.keys() :
        #             sendImageToIPThread = threading.Thread(target = self.__sendImageThread, args = (splitImageNames, key))
        #             sendImageToIPThread.start()

        # cap.release()
        # cv2.destroyAllWindows()

    def splitFrame(self, img):
        imageName = self.__createRandomName()
        splitImageThread = threading.Thread(target=self.__splitFrameToList, args=(imageName, img))
        splitImageThread.start()

    def recv(self):
        print('recv 시작')

        while True:
            receive, addr = self.__sock.recvfrom(1024)

            receive = str(receive, 'utf-8')
            recvData = self.__getRecvData(receive)

            id = recvData[0]
            code = recvData[1]
            data = recvData[2]

            print(id)
            print(code)
            print(data)

            if Code.CONN == code:
                print("CONN : ", addr)
                randomName = self.__createRandomName()
                sendMessage = Code.CONN + randomName
                self.__IP_Dict[randomName] = addr
                self.__sock.sendto(sendMessage.encode(), (addr[0], addr[1]))

            if Code.WANT == code:
                data.replace(Code.WANT, "")

                sendImageToIPThread = threading.Thread(target=self.__sendImageThread, args=(data, id))
                sendImageToIPThread.start()

            if Code.STATE == code:
                recvStr = data.split("_")
                imageName = recvStr[0].lstrip(Code.STATE)
                state = int(recvStr[1])

                if state != self.__picture_Dict[imageName][1]:
                    print(imageName, " : ", state)
                    self.__picture_Dict[imageName][1] = state

                    sendStateThread = threading.Thread(target=self.__sendStateThread,
                                                       args=(self.__createCode(Code.STATE, imageName, state), id))
                    sendStateThread.start()

    def __sendImage(self, imageName, id):
        lst = self.__picture_Dict[imageName][0]

        for bytes in lst:
            self.__send(bytes, id)
            sleep(0.001)

        print(imageName, " 전송 완료")

    def __sendImageThread(self, data: str, id):
        imageDict_copy = self.__picture_Dict.copy().keys()
        lst = list(imageDict_copy)

        if data.isdigit():
            for i in range(int(data), len(lst)):
                imageName = lst[i]
                self.__send(self.__createCode(Code.SIZE, imageName, len(self.__picture_Dict[imageName][0])), id)

        else:
            imageName = data
            sendImageThread = threading.Thread(target=self.__sendImage, args=(imageName, id))
            sendImageThread.start()

    def __sendStateThread(self, data, id):
        for key in self.__IP_Dict.keys():
            if key == id:
                continue

            self.__send(data, key)

    def __send(self, data, id: str):
        ip = self.__IP_Dict[id][0]
        port = self.__IP_Dict[id][1]
        self.__sock.sendto(data, (ip, port))

    def __splitFrameToList(self, imageName, frame):
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

        self.__picture_Dict[imageName] = [lst, 0]

    def __getCode(self, action: str, imageName: str):
        return action + imageName + " : "

    def __createCode(self, action: str, imageName: str, code):
        if type(code) != str:
            code = str(code)

        sendData = action + imageName + " : " + code

        return sendData.encode()

    def __createRandomName(self):
        chars = "abcdefghijklmnopqrstuvwsyz123456789"

        name = ""
        for i in range(8):
            name += random.choice(chars)

        return name

    def __getRecvData(self, recvData: str):
        id = recvData[0: 8]
        recvData = recvData.replace(id, "")
        recvStr = recvData.split(" : ")
        code = recvStr[0]
        data = recvStr[1]

        return (id, code, data)






