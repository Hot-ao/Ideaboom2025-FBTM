import RPi.GPIO as GPIO
import time
import sys
sys.path.append('/home/fbtm/Desktop/fbtm_code/Ideaboom2025-FBTM/RPI/app/thermal')
from capture import ThermalCapture

# Motor control pins
IN1, IN2, ENA = 23, 24, 18
ENC_A, ENC_B = 21, 25

GPIO.setmode(GPIO.BCM)

# Setup output pins individually
for pin in [IN1, IN2, ENA]:
    GPIO.setup(pin, GPIO.OUT)

# Setup input pins individually with pull-up resistor
for pin in [ENC_A, ENC_B]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# PWM setup
pwm = GPIO.PWM(ENA, 1000)
pwm.start(0)

# Control parameters
MOTOR_SPEED = 80
STEP_DEGREE = 5
MAX_STEPS = 18    # +90 degrees max
MIN_STEPS = -18   # -90 degrees min
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
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        current_step += 1

    elif direction == 'right':
        if current_step <= MIN_STEPS:
            print("Reached max right limit.")
            stop_motor()
            return
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        current_step -= 1

    else:
        stop_motor()
        return

    pwm.ChangeDutyCycle(MOTOR_SPEED)
    time.sleep(TIME_PER_STEP)
    pwm.ChangeDutyCycle(0)
    time.sleep(0.01)
    print(f"Moved {direction}. Current step: {current_step}, Angle: {current_step * STEP_DEGREE} degrees")

def stop_motor():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

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
    pwm.stop()
    GPIO.cleanup()
