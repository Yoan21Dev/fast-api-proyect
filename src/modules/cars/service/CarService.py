
from src.modules.cars.scheme.SchemeCar import CarCreate
from src.modules.cars.repositories.CarRepository import CarRepository

from src.database.db import SessionLocal
class CarService:
    def __init__(self):
        self.carRepository = CarRepository(SessionLocal)
    
    async def get_all_cars(self):
        return await self.carRepository.get_all_car()
    
    async def get_car_by_id(self, id: int):
        return await self.carRepository.get_car_by_id(id)
    
    async def create_car(self, car:CarCreate):
        return await self.carRepository.create_car(car)
    
    async def buy_car(self, user_id: int, car_id: int):
        return await self.carRepository.buy_car(user_id,car_id)