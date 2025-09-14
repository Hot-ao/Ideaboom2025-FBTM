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
    data = request.get_json(silent=True) or {} 
    for k in ("direction", "speed", "temperature", "humidity"):
        if k in data:
            _env[k] = float(data[k])
    import time
    _env["updated_ts"] = time.time()
    return jsonify({"status": "ok", "env": _env}) 
