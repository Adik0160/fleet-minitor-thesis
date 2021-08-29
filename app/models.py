from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
#from sqlalchemy.orm import relationship

from app.database import Base


class DevicesData(Base):
    __tablename__ = "devicesData"

    id = Column(Integer, primary_key=True, index=True)
    deviceNr = Column(Integer)
    fuel = Column(Integer)
    rotationSpeed = Column(Integer)
    speed = Column(Integer)
    voltage = Column(Float)

class Cars(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    deviceNr = Column(Integer)
    carName = Column(String)
    carProductionDate = Column(Integer)
    registrationName = Column(String)

    ##id##deviceNumber(foreginkey)##Nazwa samochodu##rocznik##Rejestracja##
tr = DevicesData(1, 1, 1, 1, 1, 1)
print(tr)