#import app.models as models
###############fastapi#############
import json
import asyncio
#from dotenv import load_dotenv #TODO
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Date
import uvicorn

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

############mqtt###############
import app.mqtt_module as mqtt_module

#models.Base.metadata.create_all(bind=engine)

app = FastAPI() #inicjalizacja aplikacji fast api
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(engine)

mqtt_module.mqtt.init_app(app) #inicjalizacja modułu mqtt

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/") ##### strona główna
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/list-of-things")
def readDevice(request: Request, db: Session = Depends(get_db)):
    allCars = db.query(models.Pojazdy).all()
    allDevices = db.query(models.Urzadzenia).all()
    return templates.TemplateResponse("listofthings.html", {"request": request, "allCars": allCars, "allDevices": allDevices})


@app.get("/data-viewer") ##### strona wykresów ##### domyślny pierwszy samochód lub po idiku w parametrach
async def realtime_data(request: Request, pojazdID: int = None, db: Session = Depends(get_db)):
    allCars = db.query(models.Pojazdy).all()
    actualCar = db.query(models.Pojazdy).filter(models.Pojazdy.id == pojazdID).first()
    dataFromDb = db.query(models.DaneZPojazdu).filter(models.DaneZPojazdu.pojazdID == pojazdID).all()
    #db.commit()
    return templates.TemplateResponse("dataviewer.html", {"request": request, "pojazdID": pojazdID, "allCars": allCars, "actualCar": actualCar, "dataFromDb": dataFromDb})

@app.get("/realtime-data") ##### strona wykresów ##### domyślny pierwszy samochód lub po idiku w parametrach
async def realtime_data(request: Request, pojazdID: int = None, db: Session = Depends(get_db)):
    allCars = db.query(models.Pojazdy).all()
    actualCar = db.query(models.Pojazdy).filter(models.Pojazdy.id == pojazdID).first()
    #db.commit()
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

####################################sql

