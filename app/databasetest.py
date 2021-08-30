from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, TIMESTAMP
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.sql import func
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
engine = create_engine('sqlite:///./db/dat.db', echo=True) #generujemy silnik bazodanowy to połączenia
#baza danych ma problem z samodzielnym generowaniem - żałosne

class dataFromDevices(Base): #generujemy następny model tabeli
  __tablename__ = 'dataFromDevices'
  
  id = Column(Integer, primary_key=True)
  timestamp = Column(DATETIME(fsp=6), default=func.now(), onupdate=func.now())
  deviceNr = Column(Integer)
  fuel = Column(Integer)
  rotationSpeed = Column(Integer)
  speed = Column(Integer)
  voltage = Column(Float)
  
  #addresses = relationship("Address", order_by="Address.id", backref="user")
  def __init__(self, deviceNr, fuel, rotationSpeed, speed, voltage):
      self.deviceNr = deviceNr
      self.fuel = fuel
      self.rotationSpeed = rotationSpeed
      self.speed = speed
      self.voltage = voltage

class cars(Base):
  __tablename__ = 'cars'
  
  id = Column(Integer, primary_key=True)
  deviceNr = Column(Integer)
  carName = Column(String)
  fuelType = Column(Integer)
  registrationNr = Column(String)
  productionYear = Column(Integer)
  urlLink = Column(String)
  
  #addresses = relationship("Address", order_by="Address.id", backref="user")
  def __init__(self, deviceNr, carName, fuelType, registrationNr, productionYear, urlLink):
    self.deviceNr = deviceNr
    self.carName = carName
    self.fuelType = fuelType
    self.registrationNr = registrationNr
    self.productionYear = productionYear
    self.urlLink = urlLink


Base.metadata.create_all(engine) #generujemy tabele w bazie danych

'''
class cars(Base): #generujemy model tabeli
  __tablename__ = 'cars'
  id = Column(Integer, primary_key=True)
  email_address = Column(String, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship("User", backref=backref('addresses', order_by=id))
'''  
  
'''
  Session = sessionmaker(bind=engine)
  session = Session()
  ed_user = User('ed', 'Ed Jones', 'edspassword')
  ed_user.addresses = [ Address(email_address='jack@google.com'), Address(email_address='j25@yahoo.com')]
  session.add_all([ed_user,])
  session.commit()
  for instance in session.query(User).order_by(User.id):
    print('%s - %s' % (instance.name, str(instance.addresses)))
'''







