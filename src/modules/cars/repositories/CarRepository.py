from src.modules.cars.scheme.SchemeCar import CarCreate
from src.database.models import Car 
from sqlalchemy.orm import Session
from sqlalchemy.future import select

class CarRepository : 
    
    def __init__(self, session: Session):
            self.session = session
        
        
    async def create_car(self, car_data: CarCreate):
        car_data = Car(**car_data)
        async with self.session() as session:
              session.add(car_data)
              await session.commit()
              await session.refresh(car_data)
              return car_data
          
    async def get_all_car(self):
        async with self.session() as session:
            result = await session.execute(select(Car))
            cars = result.scalars().all()
            return cars
      
        