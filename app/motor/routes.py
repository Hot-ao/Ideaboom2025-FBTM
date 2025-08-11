import socket
from flask import Blueprint, render_template, request, jsonify

motor_bp = Blueprint('motor', __name__,url_prefix='/motor')

RASPI_IP = '192.168.0.108'
RASPI_PORT = 5001

def send_to_raspi(action):
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((RASPI_IP, RASPI_PORT))
        s.sendall(action.encode())
        s.close()
    except Exception as e:
        print('Transmit error:', e)

@motor_bp.route('/input',methods=['POST'])
def input_control():
    data = request.get_json()
    action = data.get('action')
    print(f"Received action from web: {action}")

    send_to_raspi(action)

    return jsonify({'status': 'ok', 'action':action})