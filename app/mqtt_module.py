import json
from fastapi_mqtt import FastMQTT, MQTTConfig
from app.database import SessionLocal, engine
from sqlalchemy import select
import app.models as models
from app.websocket import wsManager

mqtt_config = MQTTConfig(host = "localhost",
    port= 1883,
    keepalive = 60
)

mqtt = FastMQTT(
    config=mqtt_config
)

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("data") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)
    

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    MQTTdata = json.loads(payload.decode())
    db = SessionLocal()
    urzadzenie = db.query(models.Urzadzenia).filter(models.Urzadzenia.nrUrzadzenia == MQTTdata['deviceNr']).first()
    if urzadzenie:
        print(MQTTdata['deviceNr'], " <- numerz urządzenia jest w bazie")
        tr = models.DaneZPojazdu(urzadzenie.id, MQTTdata['fuel'], MQTTdata['rotation'], MQTTdata['speed'], MQTTdata['voltage'])
        await wsManager.broadcastDataToDeviceId({"fuel": MQTTdata['fuel'], "rotation": MQTTdata['rotation'], "speed": MQTTdata['speed'], "voltage": MQTTdata['voltage']}, MQTTdata['deviceNr'])
        if urzadzenie.pojazdy:
            idPojazdu = urzadzenie.pojazdy[0].id
            tr.pojazdID = idPojazdu
        db.add(tr)
        db.commit()
        #pojazd = db.query(models.Pojazdy).join(models.Urzadzenia).filter(models.Urzadzenia.nrUrzadzenia == '1234').first()
    else:
        print(MQTTdata['deviceNr'], " <- numerz urządzenia nie istnieje w bazie")
    db.close()

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)