# app/run.py
import signal
import atexit
from threading import Thread
from app import create_app
from network.sender import run_all_senders
from network.socket_server import start_socket_server
from app.motor.module_control import update_motor_gpio, cleanup
from app.motor.pump_control import init_pump
# from app.motor.routes import start_thermal_motor_control  # �ʿ� �� ���

app = create_app()

def start_network_thread():
    t = Thread(target=run_all_senders, daemon=True)
    t.start()
    return t

def start_socket_thread():
    t = Thread(target=start_socket_server, daemon=True)
    t.start()
    return t

def start_motor_thread():
    init_pump()
    t = Thread(target=update_motor_gpio, daemon=True)
    t.start()
    return t

def graceful_shutdown(*_):
    try:
        cleanup()
    except Exception:
        pass

atexit.register(graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

if __name__ == "__main__":
    t_network = start_network_thread()
    t_socket = start_socket_thread()
    t_motor = start_motor_thread()

    try:
        app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False, threaded=True)
    finally:
        graceful_shutdown()
