from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

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