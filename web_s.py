from app import create_app
import threading
import time
import keyboard  # pip install keyboard

app = create_app()

def on_key_action(action):
    print(f"키보드 입력 감지됨: {action}")
    # 여기에 모터 제어 함수 호출 가능

def keyboard_listener():
    print("키보드 입력 감지 대기 중 (W, A, S, D / 종료: ESC)")
    while True:
        if keyboard.is_pressed('w'):
            on_key_action('forward')
            keyboard.wait('w', suppress=True)
        elif keyboard.is_pressed('a'):
            on_key_action('left')
            keyboard.wait('a', suppress=True)
        elif keyboard.is_pressed('s'):
            on_key_action('backward')
            keyboard.wait('s', suppress=True)
        elif keyboard.is_pressed('d'):
            on_key_action('right')
            keyboard.wait('d', suppress=True)
        elif keyboard.is_pressed('esc'):
            print("키보드 감지 종료")
            break
        time.sleep(0.1)

if __name__ == '__main__':
    keyboard_thread = threading.Thread(target=keyboard_listener, daemon=True)
    keyboard_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)
