# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.motor.routes import motor_bp
from app.simul.routes import simulation_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(motor_bp, url_prefix="/motor")
    app.register_blueprint(simulation_bp, url_prefix="/motor")
    return app
