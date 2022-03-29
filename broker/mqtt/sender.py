
#!/usr/bin/env python
import sys
import paho.mqtt.client as mqtt

client = mqtt.Client()

client.username_pw_set("mqtt-sender", password="<psswd>sender")
client.connect("broker.mysjid.com", 1883, 60)

topic = sys.argv[1] if len(sys.argv) > 2 else 'anonymous/info'
payload = ' '.join(sys.argv[2:]) or 'Hello World!'
client.publish(topic, payload=payload, qos=0, retain=False)
print(" [x] Sent %r:%r" % (topic, payload))