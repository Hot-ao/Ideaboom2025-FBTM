import RPi.GPIO as GPIO
import time

# Pin definition
IN1, IN2, ENA = 23, 24, 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# PWM setup
pwm = GPIO.PWM(ENA, 1000)
pwm.start(0)

step_degree = 5
max_steps = 18   # 5 degrees * 18 = 90 degrees
current_step = 0
direction = 1    # 1: forward, -1: backward
speed = 70       # Motor speed (0-100)

# Time per one revolution of motor (seconds) - measured empirically
time_per_revolution = 5.5

# Time per one step (5 degrees) calculated from one revolution time
time_per_step = time_per_revolution * (step_degree / 360)

def move_motor_step(dir):
    GPIO.output(IN1, GPIO.HIGH if dir == 1 else GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW if dir == 1 else GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)  
    time.sleep(time_per_step)
    pwm.ChangeDutyCycle(0)   # Stop motor
    time.sleep(0.1)          # Wait after stopping motor

try:
    while True:
        if current_step >= max_steps:
            direction = -1
        elif current_step <= -max_steps:
            direction = 1

        move_motor_step(direction)
        current_step += direction
        print(f"Current Step: {current_step}, Angle: {current_step * step_degree} degrees")
        time.sleep(0.05)  # Wait time between steps

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.cleanup()
