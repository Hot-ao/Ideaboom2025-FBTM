import RPi.GPIO as GPIO
import time

# Pin assignments (change according to your hardware wiring)
ENA = 18  # Motor A PWM pin
IN1 = 23  # Motor A control pin 1
IN2 = 24  # Motor A control pin 2

ENB = 13  # Motor B PWM pin
IN3 = 19  # Motor B control pin 1
IN4 = 26  # Motor B control pin 2

GPIO.setmode(GPIO.BCM)

# Set all pins as output
for pin in [ENA, IN1, IN2, ENB, IN3, IN4]:
    GPIO.setup(pin, GPIO.OUT)

# Create PWM instances for both motors
pwmA = GPIO.PWM(ENA, 1000)  # PWM frequency 1kHz for Motor A
pwmB = GPIO.PWM(ENB, 1000)  # PWM frequency 1kHz for Motor B
pwmA.start(0)  # Start PWM with 0% duty cycle (motor stopped)
pwmB.start(0)

try:
    # Move forward: set direction pins for both motors
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(90)  # Set speed to 80% for Motor A
    pwmB.ChangeDutyCycle(90)  # Set speed to 80% for Motor B
    print('Forward')
    time.sleep(5)  # Run motors for 5 seconds

    # Stop motors
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)
    print('Stop')

finally:
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
