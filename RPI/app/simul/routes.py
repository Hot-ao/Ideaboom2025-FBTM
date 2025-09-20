# app/simul/routes.py
from flask import Blueprint, request, jsonify
import time

simulation_bp = Blueprint("simulation", __name__, url_prefix="/simulation")

_env = {
    "direction": 0.0,   
    "speed": 0.0,      
    "temperature": 25.0,
    "humidity": 30.0,
    "updated_ts": 0.0,
}

def get_environment():
    #print(f"[Debug] now _env value: {_env}")
    return dict(_env)

@simulation_bp.route("/set_environment", methods=["POST"])
def set_environment():
    global _env
    try:
        data = request.get_json()
        print("aaa",request.json)
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400
        _env.update({
            "direction": data.get("direction", 0.0),
            "speed": data.get("speed", 0.0),
            "temperature": data.get("temperature", 25.0),
            "humidity": data.get("humidity", 30.0),
            "updated_ts": time.time()
        })
        #print(f"[Debug] now _env value: {_env}")
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"Exception in set_environment: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
