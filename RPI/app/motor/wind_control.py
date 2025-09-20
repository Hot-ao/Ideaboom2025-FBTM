# app/motor/wind_control.py
import time
import RPi.GPIO as GPIO

# ��ȭ�� ȹ��
import sys
sys.path.append('/home/fbtm/Desktop/fbtm_code/Ideaboom2025-FBTM/RPI/app/thermal')
from capture import ThermalCapture

# ��/�Ķ����
IN1, IN2 = 24, 25   # thermal pan A
IN3, IN4 = 22, 27   # nozzle pan B
A_PWM_PIN = 23
B_PWM_PIN = 17

GPIO.setmode(GPIO.BCM)
for pin in [IN1, IN2, IN3, IN4, A_PWM_PIN, B_PWM_PIN]:
    GPIO.setup(pin, GPIO.OUT)

# ����Ʈ���� PWM �ν��Ͻ� ���� �� ���� [RPi.GPIO PWM ����]
pwm_a = GPIO.PWM(A_PWM_PIN, 1000)
pwm_b = GPIO.PWM(B_PWM_PIN, 1000)
pwm_a.start(0)
pwm_b.start(0)
# ����: ChangeDutyCycle/stop �� PWM ���� API [web ����] [11][8][20][16]

MOTOR_SPEED = 80
STEP_DEGREE = 5
MAX_STEPS = 18
MIN_STEPS = -18
TIME_PER_REVOLUTION = 5.5
TIME_PER_STEP = TIME_PER_REVOLUTION * (STEP_DEGREE / 360.0)

CENTER = (12, 16)
TOLERANCE = 5

# �ٶ� ���� �Ķ����
ALPHA = 0.5           # ���� ���
WIND_SPEED_REF = 8.0  # m/s ȯ�� ����

thermal_step = 0  # A
nozzle_step = 0   # B

def set_dir_and_pwm(in1, in2, pwm, direction, speed=MOTOR_SPEED):
    if direction == 'left':
        GPIO.output(in1, GPIO.HIGH); GPIO.output(in2, GPIO.LOW)
    elif direction == 'right':
        GPIO.output(in1, GPIO.LOW);  GPIO.output(in2, GPIO.HIGH)
    else:
        GPIO.output(in1, GPIO.LOW);  GPIO.output(in2, GPIO.LOW)
        pwm.ChangeDutyCycle(0)
        return
    pwm.ChangeDutyCycle(speed)
    time.sleep(TIME_PER_STEP)
    pwm.ChangeDutyCycle(0)
    GPIO.output(in1, GPIO.LOW); GPIO.output(in2, GPIO.LOW)
    time.sleep(0.01)

def move_motor_step_A(direction):
    global thermal_step
    if direction == 'left':
        if thermal_step >= MAX_STEPS: return
        set_dir_and_pwm(IN1, IN2, pwm_a, 'left'); thermal_step += 1
    elif direction == 'right':
        if thermal_step <= MIN_STEPS: return
        set_dir_and_pwm(IN1, IN2, pwm_a, 'right'); thermal_step -= 1

def move_motor_step_B(direction):
    global nozzle_step
    if direction == 'left':
        if nozzle_step >= MAX_STEPS: return
        set_dir_and_pwm(IN3, IN4, pwm_b, 'left'); nozzle_step += 1
    elif direction == 'right':
        if nozzle_step <= MIN_STEPS: return
        set_dir_and_pwm(IN3, IN4, pwm_b, 'right'); nozzle_step -= 1

def stop_all():
    for pin in [IN1, IN2, IN3, IN4]:
        GPIO.output(pin, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0); pwm_b.ChangeDutyCycle(0)

def get_hotspot_position(temps):
    max_t = -1e9; pos = (0, 0)
    for i in range(len(temps)):
        for j in range(len(temps)):
            if temps[i][j] > max_t:
                max_t = temps[i][j]; pos = (i, j)
    return pos

def normalize_wind_speed_kmh_to_ms(speed_kmh):
    return speed_kmh / 3.6

def world_to_local_pan(wdir_deg_world, device_heading_deg=0.0):
    # ����(�� ����) �� ��ġ �� �� ��밢(-90~+90�� ����)
    rel = (wdir_deg_world - device_heading_deg + 540.0) % 360.0 - 180.0
    # �� �¿츸 ������ �شٰ� ����
    return max(-90.0, min(90.0, rel))

def calc_nozzle_target_angle(hotspot_angle_deg, wind_dir_world_deg, wind_speed_kmh, device_heading_deg=0.0):
    wdir_local = world_to_local_pan(wind_dir_world_deg, device_heading_deg)
    wspeed_ms = normalize_wind_speed_kmh_to_ms(wind_speed_kmh)
    wind_norm = min(max(wspeed_ms / max(WIND_SPEED_REF, 1e-6), 0.0), 2.0)
    compensation = ALPHA * wdir_local * wind_norm
    target = -hotspot_angle_deg + compensation
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

def follow_mode_adjust_nozzle(hotspot_angle_deg, wind_dir_world_deg, wind_speed_kmh, gain=0.2, device_heading_deg=0.0):
    target = calc_nozzle_target_angle(hotspot_angle_deg, wind_dir_world_deg, wind_speed_kmh, device_heading_deg)
    desired_step = int(round((target / STEP_DEGREE) * gain))
    global nozzle_step
    if desired_step > nozzle_step:
        move_motor_step_B('left')
    elif desired_step < nozzle_step:
        move_motor_step_B('right')

def control_loop(get_env_func):
    """
    get_env_func: �ֽ� ȯ�氪 dict ��ȯ �Լ� ex) simul.routes.get_environment
    """
    thermal = ThermalCapture()
    try:
        while True:
            temps = thermal.get_data()
            hotspot = get_hotspot_position(temps)
            error = hotspot[1] - CENTER[1]

            env = get_env_func()
            print(f"[DEBUG] control_loop - get_env_func return env value: {env}")         

            wind_dir = float(env.get("direction", 0.0))
            wind_spd = float(env.get("speed", 0.0))

            if abs(error) > TOLERANCE:
                if error > 0: move_motor_step_A('left')
                else:         move_motor_step_A('right')
                hotspot_angle = thermal_step * STEP_DEGREE
                follow_mode_adjust_nozzle(hotspot_angle, wind_dir, wind_spd, gain=0.2)
            else:
                hotspot_angle = thermal_step * STEP_DEGREE
                nozzle_target = calc_nozzle_target_angle(hotspot_angle, wind_dir, wind_spd)
                move_nozzle_to_angle(nozzle_target)

            time.sleep(0.01)
    finally:
        stop_all(); pwm_a.stop(); pwm_b.stop(); GPIO.cleanup()