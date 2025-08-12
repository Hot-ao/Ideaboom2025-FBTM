import time
import requests
from app.thermal.capture import ThermalCapture

SERVER_URL = 'http://192.168.0.162:5000/thermal/upload_endpoint' #MECA
#SERVER_URL = 'http://192.168.200.123:5000/thermal/upload_endpoint' #HOME

def send_thermal_data():
    thermal = ThermalCapture()
    while True:
        try:
            data = thermal.get_data()
            payload = {'data': data}
            requests.post(SERVER_URL, json=payload)
            time.sleep(0.05)
        except Exception as e:
            print("Thermal send error:", e)
        time.sleep(1)