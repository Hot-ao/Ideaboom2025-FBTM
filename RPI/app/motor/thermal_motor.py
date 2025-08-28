
import RPi.GPIO as GPIO
import time
import sys
import threading
sys.path.append('/home/fbtm/Desktop/fbtm_code/Ideaboom2025-FBTM/RPI/app/thermal')
from capture import ThermalCapture

# GPIO �� ����
IN1, IN2, ENA = 16, 20, 12
ENC_A, ENC_B = 8, 7

GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, ENA], GPIO.OUT)
GPIO.setup([ENC_A, ENC_B], GPIO.IN, pull_up_down=GPIO.PUD_UP)

# PWM ����
pwm = GPIO.PWM(ENA, 1000)
pwm.start(0)

# ���� ����
encoder_count = 0
MAX_COUNT = 1850  # ������ ȸ�� �ִ� �޽� �� ����
MIN_COUNT = -1850 # ���� ȸ�� �ּ� �޽� �� ���� (����)
MOTOR_SPEED = 70

# ���ڴ� ���ͷ�Ʈ �ݹ�
def encoder_callback(channel):
    global encoder_count
    if GPIO.input(ENC_A) == GPIO.input(ENC_B):
        encoder_count += 1
    else:
        encoder_count -= 1

GPIO.add_event_detect(ENC_A, GPIO.BOTH, callback=encoder_callback)

# ���� ���� �Լ�
def move_motor(direction, speed=MOTOR_SPEED):
    if direction == 'left':
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        pwm.ChangeDutyCycle(speed)
    elif direction == 'right':
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        pwm.ChangeDutyCycle(speed)
    else:
        stop_motor()

# ���� ���� �Լ�
def stop_motor():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

# �ʱ� ��ġ ���� �Լ� (Ȩ���� ���ư���)
def init_motor():
    global encoder_count
    print("Returning motor to home position...")
    # Ȩ ��ġ�� MIN_COUNT ��ġ�� ����, ���������� ��� ���� ����
    move_motor('right')
    while encoder_count > MIN_COUNT:
        time.sleep(0.01)
    stop_motor()
    encoder_count = 0
    print("Home position reached. Encoder count reset.")

# �ֽ��� ��ġ ã��
def get_hotspot_position(temps):
    max_temp = -9999
    pos = (0, 0)
    for i in range(len(temps)):
        for j in range(len(temps[0])):
            if temps[i][j] > max_temp:
                max_temp = temps[i][j]
                pos = (i, j)
    return pos



try:
    thermal = ThermalCapture()
    center = (12, 16)  # ��ȭ�� ���� �迭 �߾� �ε���
    tolerance = 5      # ��� ����

    while True:
        temps = thermal.get_data()
        hotspot = get_hotspot_position(temps)
        error = hotspot[1] - center[1]

        if abs(error) > tolerance:
            # ���� ȸ�� ��� ���� ���� ���� ����
            if error > 0:
                print("Move motor LEFT")
                move_motor('left')
            # ������ ȸ�� ��� ���� ���� ���� ����
            elif error < 0:
                print("Move motor RIGHT")
                move_motor('right')
            else:
                print("Limit reached, stop motor")
                stop_motor()
        else:
            print("Stop motor")
            stop_motor()

        print(f"Hotspot: {hotspot}, Encoder Count: {encoder_count}, Error: {error}")
        time.sleep(0.15)

finally:
    pwm.stop()
    GPIO.cleanup()
