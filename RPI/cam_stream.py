import requests
import cv2
from picamera2 import Picamera2
import time

#SERVER_URL = 'http://192.168.0.162:5000/stream_endpoint' #MECA
SERVER_URL = 'http://192.168.200.171:5000/stream_endpoint' #HOME

picam2 = Picamera2()
picam2.set_controls({"AwbEnable": True})
picam2.start()

while True:
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.jpg', frame)
    files = {'frame': ('image.jpg', buffer.tobytes(), 'image/jpeg')}
    try:
        requests.post(SERVER_URL, files=files, timeout=2)
    except Exception as e:
        print("error:", e)
    time.sleep(0.05)