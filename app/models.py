from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.sql import func
from app.database import Base


class Pojazdy(Base):
    __tablename__= 'POJAZDY'

    id = Column(Integer, primary_key=True)
    markaID = Column(Integer, ForeignKey('MARKI.id'))
    urzadzenieID = Column(Integer, ForeignKey('URZADZENIA.id'))
    nazwa = Column(String)
    rokProdukcji = Column(Integer)
    numerRejestracyjny = Column(String)
    zdjLink = Column(String)

    marki = relationship("Marki", back_populates='pojazdy')
    urzadzenia = relationship("Urzadzenia", back_populates='pojazdy')
    daneZPojazdu = relationship("DaneZPojazdu", back_populates='pojazdy')

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
    zdjLink = Column(String)
    
    pojazdy = relationship("Pojazdy", back_populates='urzadzenia')
    daneZPojazdu = relationship("DaneZPojazdu", back_populates='urzadzenia')

class DaneZPojazdu(Base):
    __tablename__ = 'DANE_Z_POJAZDU'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DATETIME(fsp=6), default=func.now(), onupdate=func.now())
    pojazdID = Column(Integer, ForeignKey('POJAZDY.id'))
    urzadzenieID = Column(Integer, ForeignKey('URZADZENIA.id'))
    iloscPaliwa = Column(Integer)
    predkoscObrotowa = Column(Integer)
    predkoscPojazdu = Column(Integer)
    napiecieAkumulatora = Column(Float)

    pojazdy = relationship("Pojazdy", back_populates='daneZPojazdu')
    urzadzenia = relationship("Urzadzenia", back_populates='daneZPojazdu')

    def __init__(self, urzadzenieID, iloscPaliwa, predkoscObrotowa, predkoscPojazdu, napiecieAkumulatora):
        #self.pojazdID = pojazdID
        self.urzadzenieID = urzadzenieID
        self.iloscPaliwa = iloscPaliwa
        self.predkoscObrotowa = predkoscObrotowa
        self.predkoscPojazdu = predkoscPojazdu
        self.napiecieAkumulatora = napiecieAkumulatora