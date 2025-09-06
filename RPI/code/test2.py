import RPi.GPIO as GPIO
import time
import sys
sys.path.append('/home/fbtm/Desktop/fbtm_code/Ideaboom2025-FBTM/RPI/app/thermal')
from capture import ThermalCapture

# Motor A (thermal pan) pins
IN1, IN2 = 24, 25   # A motor dir
# Motor B (nozzle pan) pins
IN3, IN4 = 22, 27   # B motor dir

# PWM pins (software PWM)
A_PWM_PIN = 23
B_PWM_PIN = 17

GPIO.setmode(GPIO.BCM)
for pin in [IN1, IN2, IN3, IN4, A_PWM_PIN, B_PWM_PIN]:
    GPIO.setup(pin, GPIO.OUT)

pwm_a = GPIO.PWM(A_PWM_PIN, 1000)  # thermal
pwm_b = GPIO.PWM(B_PWM_PIN, 1000)  # nozzle
pwm_a.start(0)
pwm_b.start(0)

# Motion params
MOTOR_SPEED = 80
STEP_DEGREE = 5
MAX_STEPS = 18     # +90 deg
MIN_STEPS = -18    # -90 deg
TIME_PER_REVOLUTION = 5.5
TIME_PER_STEP = TIME_PER_REVOLUTION * (STEP_DEGREE / 360.0)
CENTER = (12, 16)
TOLERANCE = 5

# Wind compensation params
ALPHA = 0.5          # wind influence gain (tune empirically)
WIND_SPEED_REF = 8.0 # m/s reference for normalization (tune)

# States
thermal_step = 0     # A motor
nozzle_step = 0      # B motor

def set_dir_and_pwm(in1, in2, pwm, direction, speed=MOTOR_SPEED):
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
    time.sleep(TIME_PER_STEP)
    pwm.ChangeDutyCycle(0)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    time.sleep(0.01)

def move_motor_step_A(direction):
    global thermal_step
    if direction == 'left':
        if thermal_step >= MAX_STEPS:
            print("A: max left limit")
            return
        set_dir_and_pwm(IN1, IN2, pwm_a, 'left')
        thermal_step += 1
    elif direction == 'right':
        if thermal_step <= MIN_STEPS:
            print("A: max right limit")
            return
        set_dir_and_pwm(IN1, IN2, pwm_a, 'right')
        thermal_step -= 1
    print(f"A moved {direction}. step={thermal_step}, angle={thermal_step*STEP_DEGREE}")

def move_motor_step_B(direction):
    global nozzle_step
    if direction == 'left':
        if nozzle_step >= MAX_STEPS:
            print("B: max left limit")
            return
        set_dir_and_pwm(IN3, IN4, pwm_b, 'left')
        nozzle_step += 1
    elif direction == 'right':
        if nozzle_step <= MIN_STEPS:
            print("B: max right limit")
            return
        set_dir_and_pwm(IN3, IN4, pwm_b, 'right')
        nozzle_step -= 1
    print(f"B moved {direction}. step={nozzle_step}, angle={nozzle_step*STEP_DEGREE}")

def stop_all():
    for pin in [IN1, IN2, IN3, IN4]:
        GPIO.output(pin, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

def get_hotspot_position(temps):
    max_temp = -9999
    pos = (0, 0)
    for i in range(len(temps)):
        for j in range(len(temps)):
            if temps[i][j] > max_temp:
                max_temp = temps[i][j]
                pos = (i, j)
    return pos

def calc_nozzle_target_angle(hotspot_angle_deg, wind_dir_deg, wind_speed):
    # Project wind to device pan axis; here assume wind_dir already given in same axis (−90~+90 mapped).
    # If wind_dir is 0~360 (north ref), convert to local pan frame before use.
    wind_norm = min(max(wind_speed / max(WIND_SPEED_REF, 1e-6), 0.0), 2.0)
    compensation = ALPHA * wind_dir_deg * wind_norm
    target = -hotspot_angle_deg + compensation
    # clamp and quantize to 5°
    target = max(-90, min(90, target))
    target = int(round(target / STEP_DEGREE)) * STEP_DEGREE
    return target

def move_nozzle_to_angle(target_deg):
    global nozzle_step
    target_step = int(target_deg // STEP_DEGREE)
    while nozzle_step < target_step:
        move_motor_step_B('left')
    while nozzle_step > target_step:
        move_motor_step_B('right')
    print(f"Nozzle reached target {target_deg}°")

def follow_mode_adjust_nozzle(hotspot_angle_deg, wind_dir_deg, wind_speed, gain=0.2):
    # Optional: even when not centered, let nozzle pre-bias toward target smoothly
    target = calc_nozzle_target_angle(hotspot_angle_deg, wind_dir_deg, wind_speed)
    # small step if far; scale by gain
    desired_step = int(round((target / STEP_DEGREE) * gain))
    # move at most 1 step per iteration for stability
    global nozzle_step
    if desired_step > nozzle_step:
        move_motor_step_B('left')
    elif desired_step < nozzle_step:
        move_motor_step_B('right')

try:
    thermal = ThermalCapture()

    # Example: supply wind from server; placeholders:
    wind_dir_deg = 30.0   # device-axis degrees; map from 0~360 if needed
    wind_speed = 3.0      # m/s

    while True:
        temps = thermal.get_data()
        hotspot = get_hotspot_position(temps)
        error = hotspot[21] - CENTER[21]

        if abs(error) > TOLERANCE:
            # Thermal alignment
            if error > 0:
                move_motor_step_A('left')
            else:
                move_motor_step_A('right')
            # Optional: pre-bias nozzle while aligning
            hotspot_angle = thermal_step * STEP_DEGREE
            follow_mode_adjust_nozzle(hotspot_angle, wind_dir_deg, wind_speed, gain=0.2)
        else:
            print("Hotspot centered. A motor stopped.")
            # Compute nozzle target and move decisively
            hotspot_angle = thermal_step * STEP_DEGREE
            nozzle_target = calc_nozzle_target_angle(hotspot_angle, wind_dir_deg, wind_speed)
            move_nozzle_to_angle(nozzle_target)

        print(f"Hotspot:{hotspot} Err:{error} | A_angle:{thermal_step*STEP_DEGREE} B_angle:{nozzle_step*STEP_DEGREE}")
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    stop_all()
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
