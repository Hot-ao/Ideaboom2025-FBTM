import RPi.GPIO as GPIO
import time

# Motor A control pins
IN1, IN2 = 24, 25
# Motor B control pins
IN3, IN4 = 22, 27
# PWM pins for software PWM
A_PWM_PIN = 23
B_PWM_PIN = 17

GPIO.setmode(GPIO.BCM)

# Setup output pins for motor direction and PWM
for pin in [IN1, IN2, IN3, IN4, A_PWM_PIN, B_PWM_PIN]:
    GPIO.setup(pin, GPIO.OUT)

# Software PWM setup
pwm_a = GPIO.PWM(A_PWM_PIN, 1000)
pwm_b = GPIO.PWM(B_PWM_PIN, 1000)
pwm_a.start(0)
pwm_b.start(0)

# Motion parameters
MOTOR_SPEED = 80
STEP_DEGREE = 5
MAX_STEP = 18   # +90 degrees (18 * 5)
MIN_STEP = -18  # -90 degrees
TIME_PER_REVOLUTION = 5.5
TIME_PER_STEP = TIME_PER_REVOLUTION * (STEP_DEGREE / 360)

current_step = 0
direction = 1  # 1 means moving towards +90 degrees, -1 means towards -90 degrees

def move_step(direction_str):
    if direction_str == 'left':
        # A motor left, B motor right
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
    elif direction_str == 'right':
        # A motor right, B motor left
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(MOTOR_SPEED)
    pwm_b.ChangeDutyCycle(MOTOR_SPEED)
    time.sleep(TIME_PER_STEP)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

try:
    while True:
        if direction == 1:  # Move left (towards +90)
            if current_step >= MAX_STEP:
                direction = -1  # Reverse direction
            else:
                move_step('left')
                current_step += 1
        else:  # direction == -1, Move right (towards -90)
            if current_step <= MIN_STEP:
                direction = 1  # Reverse direction
            else:
                move_step('right')
                current_step -= 1

        print(f"Current step: {current_step}, Angle: {current_step * STEP_DEGREE} degrees")
        time.sleep(0.1)  # small delay between steps

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
