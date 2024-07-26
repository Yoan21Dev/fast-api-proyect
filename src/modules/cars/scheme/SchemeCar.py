

from pydantic import BaseModel, Field

class CarCreate(BaseModel):
    name: str
    model: str
    mark: str
    year: int
    price: float
    color: str
    state: str
    created_by_user_id: int