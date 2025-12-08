# services/lights.py
import RPi.GPIO as GPIO

# Change to your actual pins
LIGHTS_PIN = 27
FOG_PIN = 22
HORN_PIN = 25

GPIO.setmode(GPIO.BCM)
for p in [LIGHTS_PIN, FOG_PIN, HORN_PIN]:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, 0)

def apply_lights(headlights: bool, fog: bool):
    GPIO.output(LIGHTS_PIN, headlights)
    GPIO.output(FOG_PIN, fog)