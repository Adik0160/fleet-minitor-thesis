from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, TIMESTAMP
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.sql import func
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import column

Base = declarative_base()
engine = create_engine('sqlite:///./db/dat2.db', connect_args={"check_same_thread": False}, echo=True) #generujemy silnik bazodanowy to połączenia
#baza danych ma problem z samodzielnym generowaniem - żałosne



''''
class daneZUrzadzen(Base): #generujemy następny model tabeli
  __tablename__ = 'DANE_Z_URZADZEN'
  
  id = Column(Integer, primary_key=True)
  timestamp = Column(DATETIME(fsp=6), default=func.now(), onupdate=func.now())
  pojazdID = Column(Integer)
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
'''


Base.metadata.create_all(engine) #generujemy tabele w bazie danych
dbsession = sessionmaker(bind=engine)

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







