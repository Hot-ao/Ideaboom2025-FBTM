import RPi.GPIO as GPIO
import time

IN1 = 23
IN2 = 24
PWM_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(PWM_PIN, GPIO.OUT)

pwm = GPIO.PWM(PWM_PIN, 100)
pwm.start(0)

def motor_forward(duration_sec, speed_percent=100):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed_percent)
    time.sleep(duration_sec)
    pwm.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

def motor_backward(duration_sec, speed_percent=100):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed_percent)
    time.sleep(duration_sec)
    pwm.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

if __name__ == "__main__":
    try:
        motor_forward(2.0)
        time.sleep(1)
        motor_forward(1.0)
    finally:
        pwm.stop()
        GPIO.cleanup()
