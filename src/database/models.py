from sqlalchemy import create_engine, Column, String, Boolean
from src.database.db import Base

# Definición del modelo de datos
class User(Base):
    
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String)
    hashed_password= Column(String)
    disabled = Column(Boolean)
    


class Car(Base):
    
    __tablename__ = "car"
    id = Column(int, primary_key=True,autoincrement=True)
    name = Column(String)
    model = Column(String)
    

