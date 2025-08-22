from flask import Blueprint, request, jsonify
from app.motor.module_control import set_motion  # motor_forward/backward 대신 set_motion 임포트

motor_bp = Blueprint("motor", __name__, url_prefix="/motor")

@motor_bp.route("/input", methods=["POST"])
def control_motor():
    data = request.get_json()
    action = data.get("action")
    print(f"Received action from web: {action}")

    if action not in ['forward', 'backward', 'left', 'right', 'stop']:
        return jsonify({"status": "error", "message": "Invalid action"}), 400

    set_motion(action)  # set_motion 으로 상태 업데이트

    return jsonify({"status": "ok", "action": action})
