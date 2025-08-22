import RPi.GPIO as GPIO
import threading
import time

LEFT_IN1 = 17
LEFT_IN2 = 18
LEFT_EN = 27
RIGHT_IN1 = 22
RIGHT_IN2 = 23
RIGHT_EN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup([LEFT_IN1, LEFT_IN2, LEFT_EN, RIGHT_IN1, RIGHT_IN2, RIGHT_EN], GPIO.OUT)

left_pwm = GPIO.PWM(LEFT_EN, 100)
right_pwm = GPIO.PWM(RIGHT_EN, 100)
left_pwm.start(0)
right_pwm.start(0)

motor_state = {'left_speed': 0, 'right_speed': 0, 'left_dir': 'stop', 'right_dir': 'stop'}
state_lock = threading.Lock()

def update_motor_gpio():
    while True:
        with state_lock:
            # 방향 제어
            GPIO.output(LEFT_IN1, GPIO.HIGH if motor_state['left_dir'] == 'forward' else GPIO.LOW)
            GPIO.output(LEFT_IN2, GPIO.HIGH if motor_state['left_dir'] == 'backward' else GPIO.LOW)
            GPIO.output(RIGHT_IN1, GPIO.HIGH if motor_state['right_dir'] == 'forward' else GPIO.LOW)
            GPIO.output(RIGHT_IN2, GPIO.HIGH if motor_state['right_dir'] == 'backward' else GPIO.LOW)
            left_pwm.ChangeDutyCycle(motor_state['left_speed'])
            right_pwm.ChangeDutyCycle(motor_state['right_speed'])
        time.sleep(0.05)

def set_motion(action):
    with state_lock:
        speed = 70
        if action == 'forward':
            motor_state['left_dir'] = 'forward'
            motor_state['right_dir'] = 'forward'
            motor_state['left_speed'] = speed
            motor_state['right_speed'] = speed
        elif action == 'backward':
            motor_state['left_dir'] = 'backward'
            motor_state['right_dir'] = 'backward'
            motor_state['left_speed'] = speed
            motor_state['right_speed'] = speed
        elif action == 'left':
            motor_state['left_dir'] = 'backward'
            motor_state['right_dir'] = 'forward'
            motor_state['left_speed'] = speed
            motor_state['right_speed'] = speed
        elif action == 'right':
            motor_state['left_dir'] = 'forward'
            motor_state['right_dir'] = 'backward'
            motor_state['left_speed'] = speed
            motor_state['right_speed'] = speed
        else: # stop
            motor_state['left_dir'] = 'stop'
            motor_state['right_dir'] = 'stop'
            motor_state['left_speed'] = 0
            motor_state['right_speed'] = 0

def cleanup():
    left_pwm.stop()
    right_pwm.stop()
    GPIO.cleanup()
