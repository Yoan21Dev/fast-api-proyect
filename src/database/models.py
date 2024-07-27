from sqlalchemy import ForeignKey, Integer, create_engine, Column, String, Boolean,Float
from src.database.db import Base
from sqlalchemy.orm import relationship
# Definición del modelo de datos
class User(Base):
    
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String,unique=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    hashed_password= Column(String)
    disabled = Column(Boolean)
    phone = Column(String)
    
    cars_created = relationship("Car", foreign_keys="Car.created_by_user_id", back_populates="creator")
    cars_bought = relationship("Car", foreign_keys="Car.sell_to_user_id", back_populates="buyer")

class Car(Base):
    __tablename__ = 'car'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    model = Column(String)
    mark = Column(String)
    state = Column(String)
    year = Column(Integer)
    price = Column(Float)
    color = Column(String)

    created_by_user_id = Column(Integer, ForeignKey('users.id'))

    sell_to_user_id = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="cars_created")
    buyer = relationship("User", foreign_keys=[sell_to_user_id], back_populates="cars_bought")


