from flask import Blueprint, request, jsonify
from app.motor.module_control import set_motion  # motor_forward/backward 대신 set_motion 임포트
from app.motor.pump_control import set_pump_state
#from app.motor.thermal_motor import ThermalMotorController

motor_bp = Blueprint("motor", __name__, url_prefix="/motor")

@motor_bp.route("/input", methods=["POST", "OPTIONS"])
def control_motor():
    if request.method == "OPTIONS":
        return "", 200
    data = request.get_json()
    action = data.get("action")
    if action not in ['forward', 'backward', 'left', 'right', 'stop']:
        return jsonify({"status": "error", "message": "Invalid action"}), 400
    set_motion(action)
    return jsonify({"status": "ok", "action": action})

@motor_bp.route('/set_environment', methods=['POST', 'OPTIONS'])
def set_environment():
    if request.method == "OPTIONS":
        return "", 200
    data = request.get_json()
    return jsonify({'status': 'success', 'received': data})

@motor_bp.route('/pump_toggle', methods=['POST', 'OPTIONS'])
def pump_toggle():
    if request.method == "OPTIONS":
        return "", 200
    data = request.get_json()
    state = data.get("state")
    if not isinstance(state, bool):
        return jsonify({"status": "error", "message": "State must be boolean"}), 400
    set_pump_state(state)
    return jsonify({"status": "ok", "pump_state": state})

"""
def start_thermal_motor_control():
    controller = ThermalMotorController()
    import time
    while True:
        controller.get_thermal_and_decide()
        time.sleep(1)
"""