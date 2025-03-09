# schemas/user.py
from pydantic import BaseModel, EmailStr

# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str

class UserBase(BaseModel):
    username: str
    email: str
    # role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    username: str
    token: str

