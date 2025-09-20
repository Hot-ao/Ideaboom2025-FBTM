import time
import RPi.GPIO as GPIO

IN1, IN2 = 24, 25   # ��ȭ�� ���� A ���� ������
IN3, IN4 = 22, 27   # ���� ���� ���� B ���� ������
A_PWM_PIN = 23
B_PWM_PIN = 17

GPIO.setmode(GPIO.BCM)
for pin in [IN1, IN2, IN3, IN4, A_PWM_PIN, B_PWM_PIN]:
    GPIO.setup(pin, GPIO.OUT)

pwm_a = GPIO.PWM(A_PWM_PIN, 1000)
pwm_b = GPIO.PWM(B_PWM_PIN, 1000)
pwm_a.start(0)
pwm_b.start(0)

def set_dir_and_pwm(in1, in2, pwm, direction, speed=80):
    if direction == 'left':
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
    elif direction == 'right':
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
    else:
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        pwm.ChangeDutyCycle(0)
        return
    pwm.ChangeDutyCycle(speed)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    time.sleep(0.1)

def move_motor_step_A(direction):
    set_dir_and_pwm(IN1, IN2, pwm_a, direction)

def move_motor_step_B(direction):
    set_dir_and_pwm(IN3, IN4, pwm_b, direction)

try:
    while True:
        print("���� A ���� ȸ��")
        move_motor_step_A('left')
        time.sleep(1)
        print("���� A ������ ȸ��")
        move_motor_step_A('right')
        time.sleep(1)
        print("���� B ���� ȸ��")
        move_motor_step_B('left')
        time.sleep(1)
        print("���� B ������ ȸ��")
        move_motor_step_B('right')
        time.sleep(1)
except KeyboardInterrupt:
    print("����: GPIO Ŭ����")
finally:
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
