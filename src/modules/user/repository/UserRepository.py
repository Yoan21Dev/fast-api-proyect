from sqlalchemy.future import select
from sqlalchemy.orm import Session
from src.modules.user.scheme.UserScheme import CreateUser
from src.database.models import User

class UserRepository():

    def __init__(self, session:Session):
      self.session = session

    async def get_all_user(self):
        async with self.session() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users

    async def create_user(self, user_data: CreateUser):

        newUser = User(username=user_data.username, hashed_password=user_data.password, email=user_data.email,disabled=user_data.disabled, full_name=user_data.full_name)

        self.session.add(newUser)
        
        await self.db_session.flush() 


        return newUser