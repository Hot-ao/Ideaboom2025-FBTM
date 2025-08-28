#app/run.py
from threading import Thread
from network.sender import run_all_senders  # 기존에 실행하던 스레드 함수
from app import create_app
from app.motor.module_control import update_motor_gpio, cleanup  # motor 제어 함수 추가
from network.socket_server import start_socket_server
from app.motor.pump_control import init_pump
#from app.motor.routes import start_thermal_motor_control

app = create_app()

def start_motor_thread():
    motor_thread = Thread(target=update_motor_gpio, daemon=True)
    motor_thread.start()
    return motor_thread

def start_socket_thread():
    socket_thread = Thread(target=start_socket_server, daemon=True)
    socket_thread.start()
    return socket_thread

def start_motor_thread():
    init_pump()
    motor_thread = Thread(target=update_motor_gpio, daemon=True)
    motor_thread.start()
    return motor_thread
"""
def start_thermal_motor_thread():
    thermal_thread = Thread(target=start_thermal_motor_control, daemon=True)
    thermal_thread.start()
    return thermal_thread
"""

if __name__ == "__main__":
    t_network = Thread(target=run_all_senders, daemon=True)
    t_network.start()

    motor_thread = start_motor_thread()
    #thermal_motor_thread = start_thermal_motor_thread()

    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        cleanup()
