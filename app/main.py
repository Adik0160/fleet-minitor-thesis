#import app.models as models
###############fastapi#############
import json
import asyncio
import uvicorn
import app.databasetest as databasetest
from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates
##############sql#################

from sqlalchemy.orm import sessionmaker
#from app.database import SessionLocal, engine

############mqtt###############
from fastapi_mqtt import FastMQTT, MQTTConfig

#models.Base.metadata.create_all(bind=engine)

MQTTnewMsg = 0
MQTTdata = 0
#def saveData():
#    session = SessionLocal()
#    tr = models.DevicesData(1, 1234, 50, 800, 75, 14.4)
#    print(tr)
#    session.add(tr)
#    session.commit()

#saveData()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

mqtt_config = MQTTConfig(host = "localhost",
    port= 1883,
    keepalive = 60
)

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)
Session = sessionmaker(bind=databasetest.engine)
session = Session()


def saveDeviceLogDB(deviceNr, fuel, rotationSpeed, speed, voltage):
    global session
    tr = databasetest.dataFromDevices(deviceNr, fuel, rotationSpeed, speed, voltage)
    session.add(tr)
    session.commit()

def saveCarsDB(deviceNr, carName, fuelType, registrationNr, productionYear):
    global session
    tr = databasetest.cars(deviceNr, carName, fuelType, registrationNr, productionYear)
    session.add(tr)
    session.commit()

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
    saveDeviceLogDB(MQTTdata['deviceNr'], MQTTdata['fuel'], MQTTdata['rotationSpeed'], MQTTdata['speed'],MQTTdata['voltage'],)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

@app.get("/car/{deviceNr}")
async def readDevice(deviceNr: int):
    global session
    return session.query(databasetest.cars).filter(databasetest.cars.deviceNr == deviceNr).first()

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        global MQTTdata
        global MQTTnewMsg
        await asyncio.sleep(0.5)
        if(MQTTnewMsg == 1):
            MQTTnewMsg = 0
            await websocket.send_json({"value" : MQTTdata['rotationSpeed']})


####################################sql

