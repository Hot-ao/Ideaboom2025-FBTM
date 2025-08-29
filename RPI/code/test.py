
import RPi.GPIO as GPIO
import time

IN1, IN2, ENA = 23, 24, 18

pulse_count = 0
last_enc_a = 0
last_enc_b = 0

GPIO.setmode(GPIO.BCM)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

pwm = GPIO.PWM(ENA, 1000)
pwm.start(70)

GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)

try:
    while True:
        print(f"Pulse count: {pulse_count}")
        time.sleep(0.005) 
except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.cleanup()
