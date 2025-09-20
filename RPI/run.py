import signal
import atexit
from threading import Thread
from app import create_app
from app.motor.module_control import update_motor_gpio, cleanup
from network.sender import run_all_senders
from network.socket_server import start_socket_server
from app.motor.pump_control import init_pump

app = create_app()

def start_motor_thread():
    """Start GPIO motor control thread."""
    init_pump()
    motor_thread = Thread(target=update_motor_gpio, daemon=True)
    motor_thread.start()
    return motor_thread

def start_socket_thread():
    """Start socket server thread."""
    socket_thread = Thread(target=start_socket_server, daemon=True)
    socket_thread.start()
    return socket_thread

def start_network_thread():
    """Start all sender threads (camera + thermal + motor)."""
    network_thread = Thread(target=run_all_senders, daemon=True)
    network_thread.start()
    return network_thread

def shutdown_handler(*args):
    """Clean up GPIO and resources on exit."""
    cleanup()
    print("? Resources cleaned up. Exiting...")

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)
atexit.register(cleanup)

if __name__ == "__main__":
    t_network = start_network_thread()
    motor_thread = start_motor_thread()
    socket_thread = start_socket_thread()

    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        shutdown_handler()
