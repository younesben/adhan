import RPi.GPIO as GPIO
import time, docker, datetime
client = docker.from_env()

from dotenv import load_dotenv
load_dotenv()

from broker.mqtt.sender import publish_and_log

#Env variables
import os 
HOME = os.environ.get('HOME')
MOSQUEE = os.environ.get('MOSQUEE')
MODE = os.environ.get('MODE')
RADIO_URL = os.environ.get('RADIO_URL')
RADIO_PORT = os.environ.get('RADIO_PORT')

MOUNT_POINT = f"{MOSQUEE}_{MODE}"

#Initialisation
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button = 17

GPIO.setup(button, GPIO.OUT)
current_state = previous_state = GPIO.input(button)


container = client.containers.get(MODE)
print(container)

try:  
    while True: 
        time.sleep(1)
        current_state = GPIO.input(button)
        if previous_state == 0 and current_state == 1:
            # turn radio on 
            container.start()
            print(f"{MOSQUEE}/start", f"http://{RADIO_URL}:{RADIO_PORT}/{MOUNT_POINT}.mp3.m3u")
            publish_and_log(f"{MOSQUEE}/info", f"Beginning of broadcast : {datetime.datetime.now()}")
            publish_and_log(f"{MOSQUEE}/start", f"http://{RADIO_URL}:{RADIO_PORT}/{MOUNT_POINT}.mp3.m3u")
            print("+++++++++")
            
        elif previous_state == 1 and current_state == 0:
            # turn radio off
            time.sleep(10)
            publish_and_log("test/stop")
            publish_and_log(f"{MOSQUEE}/info", f"End of broadcast : {datetime.datetime.now()}")
            container.stop()
            print("--------")
        previous_state = current_state
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()   

