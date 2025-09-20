import time
import requests
from app.thermal.capture import ThermalCapture

#SERVER_URL = 'http://192.168.0.162:5000/thermal/upload_endpoint' #MECA
SERVER_URL = 'http://192.168.182.251:5000/thermal/upload_endpoint' #HOME

def send_thermal_data():
    # ThermalCapture �ʱ�ȭ ��õ� ����
    while True:
        try:
            thermal = ThermalCapture()
            break
        except RuntimeError as e:
            print(f"? ThermalCapture init failed: {e}, retrying in 2s")
            time.sleep(2)

    while True:
        try:
            data = thermal.get_data()
            payload = {'data': data}

            try:
                # POST ����
                response = requests.post(SERVER_URL, json=payload, timeout=2)
                if response.status_code == 200:
                    print("?? Thermal data sent")
                else:
                    print(f"? Server response: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"? Thermal send error: {e}")

            time.sleep(0.05)  # ������ ���� �ֱ�
        except RuntimeError as e:
            print(f"? Thermal get_data error: {e}")
            time.sleep(0.1)
