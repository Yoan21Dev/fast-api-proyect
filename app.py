from fastapi import FastAPI
from src.modules.auth.controller.AuthController import authRouter
from src.modules.user.controller.UserController import userRouter
from src.database.db import create_db_and_tables
import uvicorn

app = FastAPI()

app.include_router(authRouter,tags=['Authentication route'])
app.include_router(userRouter,tags=['Users route'])

@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    return "create db"