from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
