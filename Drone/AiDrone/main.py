from DroneThread import DroneThread
from PersonDetectionThread import PersonDetectionThread
from ObjectDetectionThread import ObjectDetectionThread
from flask import Flask, render_template, Response
import cv2
from CurrentImg import Currentimg
from Server import Server

#Server = Server()

DroneTh = DroneThread()
PersonDetectionTh = PersonDetectionThread()
ObjectDetectionTh = ObjectDetectionThread()
curimg = Currentimg()


app = Flask(__name__)


def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        frame = curimg.current_pimg  # read the camera frame
        if not frame:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag.
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    # Video streaming home page.
    return render_template('index.html')



DroneTh.start()
#PersonDetectionTh.start()
#ObjectDetectionTh.start()
#Server.Start()
#app.run(host='0.0.0.0')


