import RPi.GPIO as GPIO
from time import sleep

# BCM �� ���� (��: IN1=23, IN2=24, ENA=17�� '���� ENA'�� ���)
IN2 = 27
IN1 = 22
ENA = 17   # �ϵ���� PWM �ƴ�: ����Ʈ���� PWM�� ���

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

pwm = GPIO.PWM(ENA, 1000)  # ����Ʈ���� PWM, 1 kHz ����
pwm.start(0)

try:
    # ������
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

    # �ӵ� 60%�� 1��
    pwm.ChangeDutyCycle(60)
    sleep(2)

    # ����
    pwm.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

finally:
    pwm.stop()
    GPIO.cleanup()
