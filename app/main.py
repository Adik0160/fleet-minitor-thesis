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
templates = Jinja2Templates(directory="templates")

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

@app.get("/car/{deviceNr}")
def readDevice(deviceNr: int):
    #global session
    dbsession = databasetest.dbsession()
    data = dbsession.query(databasetest.cars).filter(databasetest.cars.deviceNr == deviceNr).first()
    dbsession.close()
    return data

@app.get("/") ##### strona główna
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/chart") ##### strona wykresów ##### domyślny pierwszy samochód lub po idiku w parametrach
def chart_page(request: Request, deviceID: int = None):
    #trzeba ściagnać dane samochodu z bazy danych i wyświetlić
    dbsession = databasetest.dbsession()
    data = dbsession.query(databasetest.cars).filter(databasetest.cars.deviceNr == deviceID).first()
    print(type(data))
    dbsession.close()
    return templates.TemplateResponse("chart.html", {"request": request, "deviceID": deviceID})

@app.websocket("/{deviceID}/ws")
async def websocket_endpoint(websocket: WebSocket, deviceID):
    await websocket.accept()
    while True:
        await asyncio.sleep(0.1)
        if(mqtt_module.MQTTnewMsg == 1):
            mqtt_module.MQTTnewMsg = 0
            if(str(mqtt_module.MQTTdata['deviceNr']) == deviceID):
                await websocket.send_json({"value" : mqtt_module.MQTTdata['rotationSpeed']})


####################################sql

