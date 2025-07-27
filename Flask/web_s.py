# 가상 환경 접속 되어있는지 확인하기
# env\Scripts\activate
# cd Flask
# python web_s.py

from flask import Flask, Response, request, jsonify, render_template, send_file
import cv2
import time
#import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>Flame-Boundary-Tracking-Module</h1>
    <p>제작 중입니다.</p>
    <p>링크를 클릭하세요: <a href="/test">테스트 페이지</a></p>
    '''

# 이미지 업로딩
@app.route('/stream_endpoint', methods=['POST'])
def stream_endpoint():
    if 'frame' not in request.files:
        return jsonify({'error': 'No frame file part'}), 400
    file = request.files['frame']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    file.save('latest_cam.jpg')
    return jsonify({'status': 'success'})

@app.route('/latest_cam.jpg')
def latest_cam():
    # 최근 저장 이미지 반환
    return send_file('latest_cam.jpg', mimetype='image/jpeg')

# 이미지 스트리밍
def generate_mjpeg_stream():
    while True:
        frame = cv2.imread('latest_cam.jpg')
        if frame is not None:
            _, buffer = cv2.imencode('.jpg', frame)
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n'
            )
        time.sleep(0.05)

@app.route('/mjpeg_feed')
def mjpeg_feed():
    return Response(
        generate_mjpeg_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


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

@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5000, debug=True)
