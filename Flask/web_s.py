# 가상 환경 접속 되어있는지 확인하기
# env\Scripts\activate

from flask import Flask, Response
import cv2

app = Flask(__name__)

def gen_cam_stream():
    cap = cv2.VideoCapture("tcp://127.0.0.1:8888")  # libcamera-vid 송출주소
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        _, buffer = cv2.imencode('.jpg',frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/cam')
def cam_feed():
    return Response(gen_cam_stream(),mimetype='multipart/x-mixed-replaced; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5000, debug=True)