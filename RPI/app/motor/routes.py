# app/motor/routes.py
from flask import Blueprint, request, jsonify
from app.motor.motor_driver import motor_forward, motor_backward

motor_bp = Blueprint("motor", __name__, url_prefix="/motor")

@motor_bp.route("/input", methods=["POST"])
def control_motor():
    data = request.get_json()
    action = data.get("action")
    print(f"Received action from web: {action}")
    if action == "forward":
        motor_forward(2.0)
    elif action == "left":
        motor_forward(1.0)
    elif action == "backward":
        motor_backward(2.0)
    elif action == "right":
        motor_backward(1.0)
    else:
        return jsonify({"status": "error", "message": "invalid action"}), 400
    return jsonify({"status": "ok", "action": action})
