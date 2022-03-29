#!/usr/bin/env python
import pika
def channel_maker(username,password,host):
    credentials = pika.PlainCredentials(username,password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host,credentials=credentials,virtual_host='dev', port=5672))
    channel = connection.channel()
    return channel, connection
