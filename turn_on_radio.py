import RPi.GPIO as GPIO
import time

#Initialisation
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button = 4

GPIO.setup(button, GPIO.IN)

try:  
    while True: 
        time.sleep(2)
        if GPIO.input(button) == 1:
            # turn radio on 
            pass
            print("on")
        if GPIO.input(button) == 0:
            # turn radio off
            pass
            print("off")
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()   

