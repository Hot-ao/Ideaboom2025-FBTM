import RPi.GPIO as GPIO
import time

# Pin assignments (BCM mode)
IN1 = 5   # Direction control pin 1
IN2 = 6   # Direction control pin 2
ENA = 23  # PWM speed control pin (software PWM)

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Create PWM object on ENA pin, frequency 100Hz
pwm = GPIO.PWM(ENA, 100)
pwm.start(0)  # Start with 0% duty cycle (motor stopped)

def motor_forward(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)  # Speed control: 0 to 100%

def motor_backward(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)  # Speed control: 0 to 100%

def motor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)  # Stop PWM signal

try:
    print("Motor forward at 50% speed")
    motor_forward(100)  # Run forward at half speed
    time.sleep(2)
    motor_stop()
    time.sleep(1)
    motor_forward(50)  # Run forward at half speed
    time.sleep(2)
    motor_stop()
    time.sleep(1)
    motor_forward(20)  # Run forward at half speed
    time.sleep(2)
    motor_stop()
    time.sleep(1)
    """
    print("Motor stop")
    motor_stop()
    time.sleep(1)

    print("Motor backward at 70% speed")
    motor_backward(20)  # Run backward at 70% speed
    time.sleep(2)

    print("Motor stop")
    motor_stop()
    """
finally:
    pwm.stop()
    GPIO.cleanup()
