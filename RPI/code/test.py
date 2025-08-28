import RPi.GPIO as GPIO
import time

IN1 = 16
IN2 = 20
ENA = 12

ENC_A = 8
ENC_B = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

GPIO.setup(ENC_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENC_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pwm = GPIO.PWM(ENA, 1000)
pwm.start(0)

pulse_angle = 360 / (516 * 11)  # �� 0.0634��/�޽�
encoder_count = 0

def encoder_callback(channel):
    global encoder_count
    if GPIO.input(ENC_B) == GPIO.HIGH:
        encoder_count += 1
    else:
        encoder_count -= 1

GPIO.add_event_detect(ENC_A, GPIO.RISING, callback=encoder_callback)

def motor_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

def motor_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

def motor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

try:
    # ��ǥ ���� ����
    max_angle = 90
    min_angle = -90
    pwm.ChangeDutyCycle(50)
    
    # 90������ ȸ��
    motor_forward()
    while encoder_count * pulse_angle < max_angle:
        time.sleep(0.05)
    motor_stop()
    print("�ִ� ���� 90�� ����, ����")
    time.sleep(1)
    
    # -90������ ��ȸ��
    motor_backward()
    while encoder_count * pulse_angle > min_angle:
        time.sleep(0.05)
    motor_stop()
    print("�ּ� ���� -90�� ����, ����")

finally:
    pwm.stop()
    GPIO.cleanup()
