import json
from fastapi_mqtt import FastMQTT, MQTTConfig
from app.database import SessionLocal, engine
from sqlalchemy import select
import app.models as models
#import app.databasetest as databasetest

mqtt_config = MQTTConfig(host = "localhost",
    port= 1883,
    keepalive = 60
)

mqtt = FastMQTT(
    config=mqtt_config
)

MQTTnewMsg = 0
MQTTdata = 0

def get_db():
#    try:
        db = SessionLocal()
        yield db
 #   finally:
 #       db.close()


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("data") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)
    

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    #saveToDb()
    db = SessionLocal()
#   samochod = db.query(models.Pojazdy).filter(models.Pojazdy.urzadzenieID == '1234')
    pojazd = db.query(models.Pojazdy).filter(models.Pojazdy.urzadzenia.nrUrzadzenia == '1234').first()

    print(str(pojazd.urzadzenia))
    #global MQTTdata
    #global MQTTnewMsg
    #MQTTnewMsg = 1
    MQTTdata = json.loads(payload.decode())
    #print(type(MQTTdata))
    #dbsession = databasetest.dbsession()
    #tr = models.DaneZPojazdu(MQTTdata['deviceNr'], MQTTdata['fuel'], MQTTdata['rotationSpeed'], MQTTdata['speed'], MQTTdata['voltage'])
    #db.add(tr)
    #db.commit()
    db.close()

    #zapisz do bazy danych - asynchronicznie czy cos???
    #saveDeviceLogDB(MQTTdata['deviceNr'], MQTTdata['fuel'], MQTTdata['rotationSpeed'], MQTTdata['speed'],MQTTdata['voltage'],)
    #test githubowego klucza
@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)