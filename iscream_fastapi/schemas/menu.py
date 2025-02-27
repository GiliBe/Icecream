from pydantic import BaseModel

class MenuBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: str
    
    class Config:
        orm_mode = True

class MenuResponse(MenuBase):
    id: int
