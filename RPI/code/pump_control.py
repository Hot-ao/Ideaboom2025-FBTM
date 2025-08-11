import RPi.GPIO as GPIO
import time

# Pin assignments (BCM mode)
IN1 = 5   # Direction control pin 1
IN2 = 6   # Direction control pin 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

def motor_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

def motor_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

def motor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

try:
    print("Motor forward")
    motor_forward()
    time.sleep(5)

    print("Motor stop")
    motor_stop()
    time.sleep(2)

    print("Motor backward")
    motor_backward()
    time.sleep(5)

    print("Motor stop")
    motor_stop()

finally:
    GPIO.cleanup()
