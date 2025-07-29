from flask import Flask
from .camera import camera_bp
from .thermal import thermal_bp
from .main import main_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(camera_bp)
    app.register_blueprint(thermal_bp)
    app.register_blueprint(main_bp)
    return app