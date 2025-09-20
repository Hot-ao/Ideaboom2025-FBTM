#/app/motor/thermal_motor.py
import RPi.GPIO as GPIO
import time
import sys
sys.path.append('/home/fbtm/Desktop/fbtm_code/Ideaboom2025-FBTM/RPI/app/thermal')
from capture import ThermalCapture

# Motor A control pins
IN1, IN2 = 24, 25      # Set these to your wiring for A motor

# Motor B control pins
IN3, IN4 = 27, 22        # Set these to your wiring for B motor

# PWM pins for software PWM
A_PWM_PIN = 23         # A motor (software PWM)
B_PWM_PIN = 17         # B motor (software PWM)


GPIO.setmode(GPIO.BCM)

# Setup output pins for motor direction
for pin in [IN1, IN2, IN3, IN4, A_PWM_PIN, B_PWM_PIN]:
    GPIO.setup(pin, GPIO.OUT)

# Software PWM setup
pwm_a = GPIO.PWM(A_PWM_PIN, 1000)  # 1kHz for A motor
pwm_b = GPIO.PWM(B_PWM_PIN, 1000)  # 1kHz for B motor
pwm_a.start(0)
pwm_b.start(0)

# Control parameters
MOTOR_SPEED = 80
STEP_DEGREE = 5
MAX_STEPS = 18      # +90 degrees max
MIN_STEPS = -18     # -90 degrees min
TIME_PER_REVOLUTION = 5.5  # seconds for full revolution
TIME_PER_STEP = TIME_PER_REVOLUTION * (STEP_DEGREE / 360)
CENTER = (12, 16)
TOLERANCE = 5
current_step = 0

def move_motor_step(direction):
    global current_step
    if direction == 'left':
        if current_step >= MAX_STEPS:
            print("Reached max left limit.")
            stop_motor()
            return
        # A motor left, B motor right
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        current_step += 1
    elif direction == 'right':
        if current_step <= MIN_STEPS:
            print("Reached max right limit.")
            stop_motor()
            return
        # A motor right, B motor left
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        current_step -= 1
    else:
        stop_motor()
        return
    pwm_a.ChangeDutyCycle(MOTOR_SPEED)
    pwm_b.ChangeDutyCycle(MOTOR_SPEED)
    time.sleep(TIME_PER_STEP)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    time.sleep(0.01)
    print(f"Moved {direction}. Current step: {current_step}, Angle: {current_step * STEP_DEGREE} degrees")

def stop_motor():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

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
    while True:
        temps = thermal.get_data()
        hotspot = get_hotspot_position(temps)
        error = hotspot[1] - CENTER[1]
        if abs(error) > TOLERANCE:
            if error > 0:
                move_motor_step('left')
            else:
                move_motor_step('right')
        else:
            print("Hotspot centered. Motor stopped.")
            stop_motor()
        print(f"Hotspot: {hotspot}, Error: {error}")
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    stop_motor()
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()