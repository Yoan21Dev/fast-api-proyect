from sqlalchemy import Integer, create_engine, Column, String, Boolean,Float
from src.database.db import Base

# Definición del modelo de datos
class User(Base):
    
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String)
    full_name = Column(String)
    email = Column(String, unique=True)
    hashed_password= Column(String)
    disabled = Column(Boolean)
    phone = Column(String)
    


class Car(Base):
    
    __tablename__ = "car"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    model = Column(String)
    mark= Column(String)
    state = Column(String)
    year = Column(Integer)
    prize = Column(Float)
    color = Column(String)    

