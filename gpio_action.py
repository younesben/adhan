import RPi.GPIO as GPIO
import time

#Initialisation
button = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(button, GPIO.OUT)

if __name__ == "__main__":
    try:  
        while True: 
            GPIO.output(button, 1-GPIO.input(button))
            print(f"status changed to {GPIO.input(button)}")
            time.sleep(30)
    finally:                   # this block will run no matter how the try block exits  
        GPIO.cleanup()   