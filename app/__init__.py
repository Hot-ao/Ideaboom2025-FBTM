from flask import Flask
from .camera import camera_bp
from .thermal import thermal_bp
from .motor import motor_bp
from .main import main_bp
from .simulation import simulation_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(camera_bp)
    app.register_blueprint(thermal_bp)
    app.register_blueprint(motor_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(simulation_bp)
    return app