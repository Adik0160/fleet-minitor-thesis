import json
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates

from fastapi_mqtt import FastMQTT, MQTTConfig

MQTTnewMsg = 0
zmienna = 0

app = FastAPI()

mqtt_config = MQTTConfig(host = "localhost",
    port= 1883,
    keepalive = 60
)

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)


templates = Jinja2Templates(directory="templates")

with open('measurements.json', 'r') as file:
    measurements = iter(json.loads(file.read()))

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    global zmienna
    global MQTTnewMsg
    MQTTnewMsg = 1
    zmienna = int(payload.decode())
    print(zmienna)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/zmienna")
async def root():
    global zmienna
    return {"zmienna": zmienna}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        global zmienna
        global MQTTnewMsg
        await asyncio.sleep(0.5)
        if(MQTTnewMsg == 1):
            MQTTnewMsg = 0
            await websocket.send_json({"value" : zmienna})