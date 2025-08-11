from picamera2 import Picamera2
import cv2

class CameraCaptue:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.set_controls({"AwbEnable": True})
        self.picam2.start()
    
    def get_frame_jpg(self):
        frame = self.picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        _, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()