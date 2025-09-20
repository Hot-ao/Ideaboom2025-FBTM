import RPi.GPIO as GPIO
import time

# Motor control pins
IN1, IN2 = 24, 25  # Motor A
IN3, IN4 = 27, 22  # Motor B

# PWM pins
A_PWM_PIN = 23
B_PWM_PIN = 17

# Motor control parameters
MOTOR_SPEED = 80
STEP_DEGREE = 5
MAX_STEPS = 18
MIN_STEPS = -18
TIME_PER_REVOLUTION = 5.5
TIME_PER_STEP = TIME_PER_REVOLUTION * (STEP_DEGREE / 360)
CENTER = (12, 16)
TOLERANCE = 5

current_step = 0
pwm_a = None
pwm_b = None

def setup_gpio():
    """Initialize GPIO and PWM pins."""
    GPIO.setmode(GPIO.BCM)
    for pin in [IN1, IN2, IN3, IN4, A_PWM_PIN, B_PWM_PIN]:
        GPIO.setup(pin, GPIO.OUT)
    global pwm_a, pwm_b
    pwm_a = GPIO.PWM(A_PWM_PIN, 1000)
    pwm_b = GPIO.PWM(B_PWM_PIN, 1000)
    pwm_a.start(0)
    pwm_b.start(0)

def stop_motor():
    """Stop both motors and PWM signals."""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    if pwm_a: pwm_a.ChangeDutyCycle(0)
    if pwm_b: pwm_b.ChangeDutyCycle(0)

def move_motor_step(direction):
    """Move motors one step left or right."""
    global current_step
    if direction == 'left':
        if current_step >= MAX_STEPS:
            stop_motor()
            return
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        current_step += 1
    elif direction == 'right':
        if current_step <= MIN_STEPS:
            stop_motor()
            return
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

def get_hotspot_position(temps):
    """Find the position of the highest temperature in thermal data."""
    max_temp = -9999
    pos = (0, 0)
    for i in range(len(temps)):
        for j in range(len(temps[0])):
            if temps[i][j] > max_temp:
                max_temp = temps[i][j]
                pos = (i, j)
    return pos

def run_motor_tracking_queue(queue_motor):
    """Motor tracking loop using queue data."""
    setup_gpio()
    try:
        while True:
            temps = queue_motor.get()  # Receive thermal data from queue
            hotspot = get_hotspot_position(temps)
            error = hotspot[1] - CENTER[1]

            if abs(error) > TOLERANCE:
                if error > 0:
                    move_motor_step('left')
                else:
                    move_motor_step('right')
            else:
                stop_motor()

            print(f"Hotspot: {hotspot}, Error: {error}, Step: {current_step}")
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        stop_motor()
        if pwm_a: pwm_a.stop()
        if pwm_b: pwm_b.stop()
        GPIO.cleanup()
