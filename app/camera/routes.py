from flask import Blueprint, Response, request, jsonify, send_file
import cv2
import time

camera_bp = Blueprint('camera', __name__, url_prefix='/camera')

@camera_bp.route('/stream_endpoint', methods=['POST'])
def stream_endpoint():
    if 'frame' not in request.files:
        return jsonify({'error': 'No frame file part'}), 400
    file = request.files['frame']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    file.save('latest_cam.jpg')
    return jsonify({'status': 'success'})

@camera_bp.route('/latest_cam.jpg')
def latest_cam():
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

@camera_bp.route('/mjpeg_feed')
def mjpeg_feed():
    return Response(
        generate_mjpeg_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )