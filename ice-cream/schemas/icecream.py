from pydantic import BaseModel
from typing import Optional, List

class IceCreamBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: Optional[str] = None
    is_available: bool = True

class IceCreamCreate(IceCreamBase):
    pass

class IceCream(IceCreamBase):
    id: int

    class Config:
        orm_mode = True

