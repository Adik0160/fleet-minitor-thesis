#import app.models as models
###############fastapi#############
import json
import asyncio
from sqlalchemy.sql.expression import null
import uvicorn
#import app.databasetest as databasetest
from app.database import SessionLocal, engine
import app.models as models
from typing import List
from fastapi import FastAPI
from fastapi import Request, Depends
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.websocket import wsManager
##############sql#################

from sqlalchemy.orm import sessionmaker
#from app.database import SessionLocal, engine

############mqtt###############
import app.mqtt_module as mqtt_module

#models.Base.metadata.create_all(bind=engine)


#def saveData():
#    session = SessionLocal()
#    tr = models.DevicesData(1, 1234, 50, 800, 75, 14.4)
#    print(tr)
#    session.add(tr)
#    session.commit()

#saveData()

app = FastAPI() #inicjalizacja aplikacji fast api
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(engine)

mqtt_module.mqtt.init_app(app) #inicjalizacja modułu mqtt

'''
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
'''
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/test")
async def readDevice(request: Request, deviceNr: str = None):
    await manager.broadcastDataToDeviceId(deviceNr, deviceNr)
    return 'OK'

@app.get("/car")
def readDevice(carNr: int = None, db: Session = Depends(get_db)):
    if carNr == None:
        samochody = db.query(models.Pojazdy).all()
    return samochody

@app.get("/") ##### strona główna
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/realtime-data") ##### strona wykresów ##### domyślny pierwszy samochód lub po idiku w parametrach
async def chart_page(request: Request, pojazdID: int = None, db: Session = Depends(get_db)):
    allCars = db.query(models.Pojazdy).all()
    actualCar = db.query(models.Pojazdy).filter(models.Pojazdy.id == pojazdID).first()
    db.commit()
    return templates.TemplateResponse("realtime.html", {"request": request, "pojazdID": pojazdID, "allCars": allCars, "actualCar": actualCar})

@app.websocket("/ws/{deviceNr}")
async def websocket_endpoint(websocket: WebSocket, deviceNr: int):
    await wsManager.connect(websocket, deviceNr)
    try:
        while True:
            await websocket.receive_text()
            #await manager.send_personal_message(f"You wrote: {data}", websocket)
            #await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        wsManager.disconnect(websocket)
 #       await manager.broadcast(f"Client #{client_id} left the chat")

'''
@app.websocket("/{deviceID}/ws")
async def websocket_endpoint(websocket: WebSocket, deviceID):
    await websocket.accept()
    while True:
        await asyncio.sleep(0.1)
        if(mqtt_module.MQTTnewMsg == 1):
            mqtt_module.MQTTnewMsg = 0
            if(str(mqtt_module.MQTTdata['deviceNr']) == deviceID):
                await websocket.send_json({"value" : mqtt_module.MQTTdata['rotationSpeed']})

'''
####################################sql

