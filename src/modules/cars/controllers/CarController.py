from fastapi import APIRouter


carController = APIRouter()

@carController.post()
async def create_car(car: dict):
    return {"message": "Car created successfully"}