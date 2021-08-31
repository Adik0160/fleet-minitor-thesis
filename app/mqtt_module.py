import json
from fastapi_mqtt import FastMQTT, MQTTConfig
import app.databasetest as databasetest

mqtt_config = MQTTConfig(host = "localhost",
    port= 1883,
    keepalive = 60
)

mqtt = FastMQTT(
    config=mqtt_config
)

MQTTnewMsg = 0
MQTTdata = 0

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("data") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)
    

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    #saveToDb()
    global MQTTdata
    global MQTTnewMsg
    MQTTnewMsg = 1
    MQTTdata = json.loads(payload.decode())
    print(type(MQTTdata))
    dbsession = databasetest.dbsession()
    tr = databasetest.dataFromDevices(MQTTdata['deviceNr'], MQTTdata['fuel'], MQTTdata['rotationSpeed'], MQTTdata['speed'], MQTTdata['voltage'])
    dbsession.add(tr)
    dbsession.commit()
    dbsession.close()

    #zapisz do bazy danych - asynchronicznie czy cos???
    #saveDeviceLogDB(MQTTdata['deviceNr'], MQTTdata['fuel'], MQTTdata['rotationSpeed'], MQTTdata['speed'],MQTTdata['voltage'],)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)