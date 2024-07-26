from src.modules.cars.scheme.SchemeCar import CarCreate
from src.database.models import Car 
from sqlalchemy.orm import Session
from sqlalchemy.future import select

class CarRepository : 
    
    def __init__(self, session: Session):
            self.session = session
        
        
    async def create_car(self, car_data: CarCreate):
        car_data = Car(name = car_data.name,model = car_data.model,
                       mark = car_data.mark,
                       state = car_data.state,
                       year = car_data.year,
                    price = car_data.price,
                    color = car_data.color,
                    created_by_user_id = car_data.created_by_user_id)
        print(car_data)
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
      
    async def buy_car(self, user_id: int, car_id: int):
        async with self.session() as session:
            # Obtener el coche por ID
            result = await session.execute(select(Car).where(Car.id == car_id))
            car = result.scalar_one_or_none()
            
            if not car:
                return False  # El coche no existe

            car.sell_to_user_id = user_id  # Asignar el coche al usuario

            session.add(car)
            await session.commit()

            return True