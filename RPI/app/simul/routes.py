# app/simul/routes.py
from flask import Blueprint, request, jsonify

simulation_bp = Blueprint("simulation", __name__, url_prefix="/simulation")

_env = {
    "direction": 0.0,   
    "speed": 0.0,      
    "temperature": 25.0,
    "humidity": 30.0,
    "updated_ts": 0.0,
}

def get_environment():
    return dict(_env)

@simulation_bp.route("/set_environment", methods=["POST"])
def set_environment():
    data = request.get_json(silent=False) 
    i=1
    try:
        direction = float(data["direction"]); speed = float(data["speed"])
        temperature = float(data["temperature"]); humidity = float(data["humidity"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"status": "error", "message": "invalid or missing fields"}), 400
        #return 0
    direction = direction % 360.0
    humidity = max(0.0, min(100.0, humidity))

    _env.update({
        "direction": direction,
        "speed": speed,
        "temperature": temperature,
        "humidity": humidity,
    })
    import time
    _env["updated_ts"] = time.time()
    return jsonify({"status": "ok", "env": _env}), 200
    #return 0

