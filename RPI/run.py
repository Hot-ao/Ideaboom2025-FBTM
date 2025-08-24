#app/run.py
from threading import Thread
from network.sender import run_all_senders  # 기존에 실행하던 스레드 함수
from app import create_app
from app.motor.module_control import update_motor_gpio, cleanup  # motor 제어 함수 추가
from network.socket_server import start_socket_server
app = create_app()

def start_motor_thread():
    motor_thread = Thread(target=update_motor_gpio, daemon=True)
    motor_thread.start()
    return motor_thread

def start_socket_thread():
    socket_thread = Thread(target=start_socket_server, daemon=True)
    socket_thread.start()
    return socket_thread


if __name__ == "__main__":
    # 기존 네트워크 관련 스레드 시작
    t_network = Thread(target=run_all_senders, daemon=True)
    t_network.start()

    # 모터 제어 스레드 시작 추가
    motor_thread = start_motor_thread()

    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        cleanup()
