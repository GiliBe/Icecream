from pydantic import BaseModel
from typing import Optional

class OrderBase(BaseModel):
    user_id: int
    status: str

    class Config:
        orm_mode = True

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int

