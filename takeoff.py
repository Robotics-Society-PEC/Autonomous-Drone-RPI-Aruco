import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)

while True:
    print(GPIO.input(23))
    time.sleep(0.3)