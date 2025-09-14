import RPi.GPIO as GPIO

PUMP_PIN = 5 

def init_pump():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PUMP_PIN, GPIO.OUT)
    GPIO.output(PUMP_PIN, GPIO.HIGH)  # �⺻ OFF

def set_pump_state(state: bool):
    GPIO.output(PUMP_PIN, GPIO.HIGH if state else GPIO.LOW)
