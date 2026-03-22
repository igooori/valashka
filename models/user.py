from sqlalchemy import Column,Integer,String,DateTime,Boolean,create_engine,BigInteger,Float,DateTime,JSON  
from sqlalchemy.orm import DeclarativeBase,Session
import datetime
engine = create_engine('sqlite:///bases/user.db')
class Base(DeclarativeBase): pass
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    user_id = Column(BigInteger,unique=True)
    subscription_end = Column(DateTime,nullable=True)
    created_at = Column(DateTime,default=datetime.datetime.utcnow)
class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    payment_id = Column(String, unique=True)
    amount_rub = Column(Float)
    amount_usdt = Column(Float) 
    currency = Column(String, default='RUB')
    payment_system = Column(String)  
    status = Column(String, default='pending')
    product_type = Column(String)    
    tariff_period = Column(String)   
    created_at = Column(DateTime, default=datetime.datetime.now)
    paid_at = Column(DateTime)
class Tiket(Base):
    __tablename__ = 'tikets'
    id = Column(Integer,primary_key=True)
    user_id = Column(BigInteger)
    username = Column(String)
    status = Column(String,default='open')
    create_at = Column(DateTime,default=datetime.datetime.utcnow)
    message = Column(String)
class Applications(Base):
    __tablename__ = 'applications'
    id = Column(Integer,primary_key=True)
    user_id = Column(BigInteger,nullable=False)
    answers = Column(JSON)
    created_at = Column(DateTime,default=datetime.datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    reviewed_by = Column(BigInteger, nullable=True)
Base.metadata.create_all(bind=engine)
