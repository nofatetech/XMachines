# services/motors.py
import RPi.GPIO as GPIO

# ←←← CHANGE THESE TO YOUR ACTUAL PINOUT ←←←
LEFT_IN1 = 17
LEFT_IN2 = 18
RIGHT_IN1 = 22
RIGHT_IN2 = 23
LEFT_EN = 12   # PWM pin
RIGHT_EN = 13  # PWM pin

GPIO.setmode(GPIO.BCM)
for pin in [LEFT_IN1, LEFT_IN2, RIGHT_IN1, RIGHT_IN2, LEFT_EN, RIGHT_EN]:
    GPIO.setup(pin, GPIO.OUT)

pwm_left = GPIO.PWM(LEFT_EN, 1000)
pwm_right = GPIO.PWM(RIGHT_EN, 1000)
pwm_left.start(0)
pwm_right.start(0)

def set_tank_drive(left_percent: int, right_percent: int):
    # left_percent, right_percent = -100..100

    def drive_side(in1, in2, pwm, speed):
        if speed = max(-100, min(100, speed))
        if speed > 0:
            GPIO.output(in1, 1); GPIO.output(in2, 0)
            pwm.ChangeDutyCycle(speed)
        elif speed < 0:
            GPIO.output(in1, 0); GPIO.output(in2, 1)
            pwm.ChangeDutyCycle(-speed)
        else:
            GPIO.output(in1, 0); GPIO.output(in2, 0)
            pwm.ChangeDutyCycle(0)

    drive_side(LEFT_IN1, LEFT_IN2, pwm_left, left_percent)
    drive_side(RIGHT_IN1, RIGHT_IN2, pwm_right, right_percent)