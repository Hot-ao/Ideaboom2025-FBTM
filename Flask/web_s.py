# 가상 환경 접속 되어있는지 확인하기
# env\Scripts\activate

from flask import Flask, Response, request, jsonify, render_template
import numpy as np
import cv2

app = Flask(__name__)

def gen_cam_stream():
    cap = cv2.VideoCapture("tcp://192.168.0.8:8888")  # libcamera-vid 송출주소
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        _, buffer = cv2.imencode('.jpg',frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
@app.route('/')
def index():
    return '''
    <h1>Flame-Boundary-Tracking-Module</h1>
    <p>제작 중입니다.</p>
    <p>링크를 클릭하세요: <a href="/cam">/ cam</a></p>
    <img src="/cam" width = "480">
    '''

# 캠 송출
@app.route('/cam')
def cam_feed():
    return Response(gen_cam_stream(),mimetype='multipart/x-mixed-replace; boundary=frame')

# MLX90640 송출
latest_data = None

@app.route('/upload_endpoint', methods=['POST'])
def upload():
    global latest_data
    content = request.get_json()
    latest_data = content['data']
    return jsonify({'status': 'success'})

@app.route('/thermal-data')
def thermal_data():
    global latest_data
    if latest_data is None:
        return jsonify({'error': 'No data yet'}), 404
    return jsonify({'data': latest_data})

@app.route('/thermal-visual')
def thermal_visual():
    return render_template('thermal.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5000, debug=True)
