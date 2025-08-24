import socket
from app.motor.module_control import set_motion

def start_socket_server(host='0.0.0.0', port=5001):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((host, port))
    server_sock.listen(1)
    print(f"Socket server started on {host}:{port}")

    try:
        while True:
            client_sock, addr = server_sock.accept()
            print(f"Connection from {addr}")

            data = client_sock.recv(1024)
            if data:
                action = data.decode().strip()
                print(f"Received action from main server: {action}")
                # ��ȿ�� �������� üũ �� ���� ���� �Լ� ȣ��
                if action in ['forward', 'backward', 'left', 'right', 'stop']:
                    set_motion(action)
                else:
                    print("Invalid action received:", action)
            client_sock.close()
    except KeyboardInterrupt:
        print("Socket server stopping.")
    finally:
        server_sock.close()
