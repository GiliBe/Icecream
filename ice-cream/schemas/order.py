
from pydantic import BaseModel
from typing import Optional, List

class OrderItemBase(BaseModel):
    icecream_id: int
    quantity: int
    unit_price: float

class OrderCreate(BaseModel):
    items: List[OrderItemBase]

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    items: List[OrderItem]

    class Config:
        orm_mode = True