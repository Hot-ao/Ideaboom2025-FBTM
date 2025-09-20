import time
import requests
from app.camera.capture import CameraCaptue

#SERVER_URL = 'http://192.168.0.162:5000/camera/stream_endpoint' #MECA
SERVER_URL = 'http://192.168.182.251:5000/camera/stream_endpoint' #HOME

def send_camera_stream():
    cam = CameraCaptue()
    while True:
        try:
            jpg_bytes = cam.get_frame_jpg()
            files = {'frame': ('image.jpg', jpg_bytes, 'image/jpeg')}
            requests.post(SERVER_URL, files=files, timeout=2)
        except Exception as e:
            print("Camera send error:", e)
        time.sleep(0.05)