#import app.models as models
###############fastapi#############
import json
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates
##############sql#################
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
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

mqtt_config = MQTTConfig(host = "localhost",
    port= 1883,
    keepalive = 60
)

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)


templates = Jinja2Templates(directory="templates")



@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("data") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)
    

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    global MQTTdata
    global MQTTnewMsg
    MQTTnewMsg = 1
    MQTTdata = json.loads(payload.decode())

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
    global MQTTdata
    return {MQTTdata}

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

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  
  id = Column(Integer, primary_key=True)
  name = Column(String)
  fullname = Column(String)
  password = Column(String)
  
  #addresses = relationship("Address", order_by="Address.id", backref="user")
  def __init__(self, name, fullname, password):
      self.name = name
      self.fullname = fullname
      self.password = password

  def __repr__(self):
     return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

class Address(Base):
  __tablename__ = 'addresses'
  id = Column(Integer, primary_key=True)
  email_address = Column(String, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship("User", backref=backref('addresses', order_by=id))

  def __init__(self, email_address):
      self.email_address = email_address

  def __repr__(self):
      return "<Address('%s')>" % self.email_address

engine = create_engine('sqlite:///:memory:', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

ed_user = User('ed', 'Ed Jones', 'edspassword')
ed_user.addresses = [
 Address(email_address='jack@google.com'),
 Address(email_address='j25@yahoo.com')]
session.add_all([ed_user,])
session.commit()


for instance in session.query(User).order_by(User.id):
  print ('%s - %s' % (instance.name, str(instance.addresses)))