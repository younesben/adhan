#!/usr/bin/env python
import sys
import os
import paho.mqtt.client as mqtt

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

print(' [*] Waiting for logs. To exit press CTRL+C')

client = mqtt.Client()
client.username_pw_set("mqtt-worker", password="<psswd>worker")
client.connect("broker.mysjid.com", 1883, 60)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("test/#")
client.on_connect = on_connect

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f" [x] {msg.topic}:{ msg.payload.decode('utf-8')}")
    with open(f"{os.getcwd()}/logs/broadcast.txt", 'ab') as f:
        f.write(msg.payload)
        f.write(b'\n')
client.on_message = on_message

client.loop_forever()