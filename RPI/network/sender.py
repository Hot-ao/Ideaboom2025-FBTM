from threading import Thread
from queue import Queue
import time
import requests
from network.camera_sender import send_camera_stream
from app.motor.thermal_motor import run_motor_tracking_queue
from app.thermal.capture import ThermalCapture

# Queues for sharing thermal data
queue_server = Queue(maxsize=10)
queue_motor = Queue(maxsize=10)

# Thread to read thermal data
def thermal_reader():
    """Read thermal data from MLX90640 and distribute to queues."""
    thermal = None
    while thermal is None:
        try:
            thermal = ThermalCapture()
        except RuntimeError as e:
            print(f"? ThermalCapture init failed: {e}, retrying in 2s")
            time.sleep(2)

    while True:
        data = thermal.get_data()
        if not queue_server.full():
            queue_server.put(data)
        if not queue_motor.full():
            queue_motor.put(data)
        time.sleep(0.05)

# Thread to send thermal data to server
def send_thermal_data():
    """Send thermal data to main server."""
    SERVER_URL = 'http://192.168.182.251:5000/thermal/upload_endpoint'
    while True:
        data = queue_server.get()
        try:
            response = requests.post(SERVER_URL, json={'data': data}, timeout=2)
            if response.status_code == 200:
                print("?? Thermal data sent")
            else:
                print(f"? Server response: {response.status_code}")
        except Exception as e:
            print(f"? Thermal send error: {e}")
        time.sleep(0.05)

# Thread to run motor control
def motor_control_thread():
    """Consume thermal data from queue and control motors."""
    run_motor_tracking_queue(queue_motor)

# Run all sender and control threads
def run_all_senders():
    """Start camera, thermal reader, thermal sender, and motor control threads."""
    t_camera = Thread(target=send_camera_stream, daemon=True)
    t_camera.start()
    print("?? Camera sender started")

    t_reader = Thread(target=thermal_reader, daemon=True)
    t_reader.start()
    print("??? Thermal reader started")

    t_thermal = Thread(target=send_thermal_data, daemon=True)
    t_thermal.start()
    print("?? Thermal sender started")

    t_motor = Thread(target=motor_control_thread, daemon=True)
    t_motor.start()
    print("?? Motor control started")

    # Monitor threads and restart if any thread stops
    while True:
        for t_name, t in [('camera', t_camera), ('thermal', t_thermal),
                          ('reader', t_reader), ('motor', t_motor)]:
            if not t.is_alive():
                print(f"? {t_name} thread stopped, restarting...")
                if t_name == 'camera':
                    t_camera = Thread(target=send_camera_stream, daemon=True)
                    t_camera.start()
                elif t_name == 'thermal':
                    t_thermal = Thread(target=send_thermal_data, daemon=True)
                    t_thermal.start()
                elif t_name == 'reader':
                    t_reader = Thread(target=thermal_reader, daemon=True)
                    t_reader.start()
                elif t_name == 'motor':
                    t_motor = Thread(target=motor_control_thread, daemon=True)
                    t_motor.start()
        time.sleep(5)
