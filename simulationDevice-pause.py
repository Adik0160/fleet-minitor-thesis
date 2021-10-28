# python 3.6

import random
import time
import json
import sys


from paho.mqtt import client as mqtt_client

deviceNr = 1234
speed = 50
broker = 'localhost'
port = 1883
topic = "data"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    global deviceNr
    global speed
    while True:
        #time.sleep(1)
        input("nacisnij klawisz opublikować")
        msg = json.dumps({"deviceNr": deviceNr, "fuel": 50, "rotation": random.randrange(1200, 1500, 1), "speed": random.randrange(speed, speed+35, 1), "voltage": 14.4})
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    args = sys.argv[1:]
    global deviceNr
    global speed
    deviceNr = int(args[0])
    speed = int(args[1])
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()