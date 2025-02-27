from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
