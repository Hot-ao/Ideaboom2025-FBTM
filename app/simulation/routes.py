from flask import Blueprint, render_template, jsonify
import random

simulation_bp = Blueprint('simulation', __name__, url_prefix='/simulation')

def generate_wind_data():
    return {
        "direction": random.randint(0, 360),  # 풍향 (도)
        "speed": round(random.uniform(0, 80), 1),  # 풍속 (km/h)
        "temperature": round(random.uniform(20, 50), 1),  # 대기 온도 (도)
        "humidity": round(random.uniform(5, 50), 1),  # 상대습도 (%)
    }

@simulation_bp.route('/')
def simulation():
    return render_template('simulation.html')

@simulation_bp.route('/data')
def simulation_data():
    data = generate_wind_data()
    return jsonify(data)
