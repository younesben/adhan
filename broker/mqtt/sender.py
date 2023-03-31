
#!/usr/bin/env python
import sys
import paho.mqtt.client as mqtt

client = mqtt.Client()

client.username_pw_set("mqtt-sender", password="<psswd>sender")
client.connect("broker.mysjid.com", 1883, 60)

def publish_and_log(topic, payload=''):
    client.publish(topic, payload=payload, qos=0, retain=False)
    print(" [x] Sent %r:%r" % (topic, payload))

if __name__ == "__main__":
    topic = sys.argv[1]
    payload = ' '.join(sys.argv[2:]) or 'Hello World!'

    publish_and_log(topic, payload)