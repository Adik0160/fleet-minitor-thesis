from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
#from app.database import Base
#from sqlalchemy.orm import relationship

from app.database import Base


class Pojazdy(Base):
  __tablename__= 'POJAZDY'

  id = Column(Integer, primary_key=True)
  markaID = Column(Integer, ForeignKey('MARKI.id'))
  nazwa = Column(String)
  rokProdukcji = Column(Integer)
  numerRejestracyjny = Column(String)
  predkoscMax = Column(Integer)
  #zdjLink = Column(String)

  marki = relationship("Marki", back_populates='pojazdy')
  przypisanie = relationship("Przypisanie", back_populates='pojazdy')

class Marki(Base):
  __tablename__= 'MARKI'

  id = Column(Integer, primary_key=True)
  nazwaMarki = Column(String)
  panstwo = Column(String)

  pojazdy = relationship("Pojazdy", back_populates='marki')

class Urzadzenia(Base):
  __tablename__= 'URZADZENIA'

  id = Column(Integer, primary_key=True)
  nrUrzadzenia = Column(String)

  przypisanie = relationship("Przypisanie", back_populates='urzadzenia')

class Przypisanie(Base):
  __tablename__= 'PRZYPISANIE'

  id = Column(Integer, primary_key=True)
  pojazdID = Column(Integer, ForeignKey('POJAZDY.id'))
  urzadzenieID = Column(Integer, ForeignKey('URZADZENIA.id'))

  pojazdy = relationship("Pojazdy", back_populates='przypisanie')
  urzadzenia = relationship("Urzadzenia", back_populates='przypisanie')