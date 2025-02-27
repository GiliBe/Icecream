from pydantic import BaseModel

class MaterialBase(BaseModel):
    name: str
    quantity: int

    class Config:
        orm_mode = True

class MaterialCreate(MaterialBase):
    pass

class MaterialResponse(MaterialBase):
    id: int
