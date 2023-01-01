import logging
import socket
import os
import sys
import threading
import time
import subprocess
import numpy as np
import cv2

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

DEFAULT_DISTANCE = 0.30
DEFAULT_DEGREE = 10

FRAME_X = int(960/3)
FRAME_Y = int(720/3)
FRAME_AREA = FRAME_X * FRAME_Y

FRAME_SIZE = FRAME_AREA * 3
FRAME_CENTER_X = FRAME_X / 2
FRAME_CENTER_Y = FRAME_Y / 2

CMD_FFMPEG = (f'ffmpeg -hwaccel auto -hwaccel_device opencl -i pipe:0 '
              f'-pix_fmt bgr24 -s {FRAME_X}x{FRAME_Y} -f rawvideo pipe:1')

FACE_DETECT_XML_FILE = 'haarcascade_frontalface_default.xml'


class ErrorNoFaceDetectXMLFile(Exception):
    """Error no face detect xml file"""


class MyDrone(object):
    def __init__(self, host_ip='192.168.10.2', host_port=8889,
                 drone_ip='192.168.10.1', drone_port=8889,
                 is_imperial=False):
        self.host_ip = host_ip
        self.host_port = host_port
        self.drone_ip = drone_ip
        self.drone_port = drone_port
        self.drone_address = (drone_ip, drone_port)
        self.is_imperial = is_imperial

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host_ip, self.host_port))

        self.response = None
        self.stop_event = threading.Event()

        # thread for receiving cmd ack
        self._response_thread = threading.Thread(
            target=self.receive_response,
            args=(self.stop_event, ))
        # self._response_thread.daemon = True
        self._response_thread.start()

        self.proc = subprocess.Popen(CMD_FFMPEG.split(' '),
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE)
        self.proc_stdin = self.proc.stdin
        self.proc_stdout = self.proc.stdout

        # thread for receiving video
        self.video_port = 11111

        self._receive_video_thread = threading.Thread(
            target=self.receive_video,
            args=(self.stop_event, self.proc_stdin,
                  self.host_ip, self.video_port,))
        self._receive_video_thread.start()

        # for person detection
        if not os.path.exists(FACE_DETECT_XML_FILE):
            raise ErrorNoFaceDetectXMLFile(f'No {FACE_DETECT_XML_FILE}')
        self.face_cascade = cv2.CascadeClassifier(FACE_DETECT_XML_FILE)
        self._is_enable_face_detect = False

        self.send_command('command')
        self.send_command('streamon')

    def receive_response(self, stop_event):
        while not stop_event.is_set():
            try:
                self.response, ip = self.socket.recvfrom(3000)
                logger.info({'action': 'receive_response',
                             'response': self.response})
            except socket.error as ex:
                logger.error({'action': 'receive_response',
                             'ex': ex})
                break

    def __dell__(self):
        self.stop()

    def stop(self):
        self.stop_event.set()
        retry = 0
        while self._response_thread.isAlive():
            time.sleep(0.3)
            if retry > 30:
                break
            retry += 1
        self.socket.close()
        os.kill(self.proc.pid, 9)

    def send_command(self, command):
        logger.info({'action': 'send_command', 'command': command})
        self.socket.sendto(command.encode('utf-8'), self.drone_address)

        retry = 0
        while self.response is None:
            time.sleep(0.3)
            if retry > 3:
                break
            retry += 1

        if self.response is None:
            response = None
        else:
            response = self.response.decode('utf-8')
        self.response = None
        return response

    # def takeoff(self):
    #     return self.send_command('takeoff')
    #
    # def land(self):
    #     return self.send_command('land')
    #
    # def move(self, direction, distance):
    #     distance = float(distance)
    #     if self.is_imperial:
    #         distance = int(round(distance * 30.48))
    #     else:
    #         distance = int(round(distance * 100))
    #     return self.send_command(f'{direction} {distance}')
    #
    # def up(self, distance=DEFAULT_DISTANCE):
    #     return self.move('up', distance)
    #
    # def down(self, distance=DEFAULT_DISTANCE):
    #     return self.move('down', distance)
    #
    # def left(self, distance=DEFAULT_DISTANCE):
    #     return self.move('left', distance)
    #
    # def right(self, distance=DEFAULT_DISTANCE):
    #     return self.move('right', distance)
    #
    # def forward(self, distance=DEFAULT_DISTANCE):
    #     return self.move('forward', distance)
    #
    # def back(self, distance=DEFAULT_DISTANCE):
    #     return self.move('back', distance)
    #
    # def set_speed(self, speed):
    #     return self.send_command(f'speed {speed}')
    #
    # def clockwise(self, degree=DEFAULT_DEGREE):
    #     return self.send_command(f'cw {degree}')
    #
    # def counter_clockwise(self, degree=DEFAULT_DEGREE):
    #     return self.send_command(f'ccw {degree}')
    #
    # def flip_front(self):
    #     return self.send_command('flip f')
    #
    # def flip_back(self):
    #     return self.send_command('flip b')
    #
    # def flip_left(self):
    #     return self.send_command('flip l')
    #
    # def flip_right(self):
    #     return self.send_command('flip r')

    def receive_video(self, stop_event, pipe_in, host_ip, video_port):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_video:
            sock_video.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock_video.settimeout(.5)
            sock_video.bind((host_ip, video_port))
            data = bytearray(2048)
            while not stop_event.is_set():
                try:
                    size, addr = sock_video.recvfrom_into(data)
                    # logger.info({'action': 'receive_video', 'data': data})
                except socket.timeout as ex:
                    logger.warning({'action': 'receive_video', 'ex': ex })
                    time.sleep(0.5)
                    continue
                except socket.error as ex:
                    logger.error({'action': 'receive_video', 'ex': ex})
                    break

                try:
                    pipe_in.write(data[:size])
                    pipe_in.flush()
                except Exception as ex:
                    logger.error({'action': 'receive_video', 'ex': ex})
                    break

    def enable_face_detect(self):
        self._is_enable_face_detect = True

    def disable_face_detect(self):
        self._is_enable_face_detect = False

    def video_binary_generator(self):
        while True:
            try:
                frame = self.proc_stdout.read(FRAME_SIZE)
            except Exception as ex:
                logger.error({'action': 'video_binary_generator', 'ex': ex})
                continue

            if not frame:
                continue

            frame = np.fromstring(frame, np.uint8).reshape(FRAME_Y, FRAME_X, 3)

            # person detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, 'person', (x, y-6), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)

            cv2.imshow('Drone View', frame)
            # yield frame

if __name__ == '__main__':
    file_name = sys.argv[1]

    f = open(file_name, "r")
    commands = f.readlines()

    MyDrone = MyDrone()

    for command in commands:
        if command != '' and command != '\n':
            command = command.rstrip()

            if command.find('delay') != -1:
                sec = float(command.partition('delay')[2])
                print('delay %s' % sec)
                time.sleep(sec)
                pass
            else:
                MyDrone.send_command(command)
                # print(command)

    MyDrone.video_binary_generator()

    MyDrone.stop()
