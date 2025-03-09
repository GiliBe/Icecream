# models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from db.connection import Base
from sqlalchemy.orm import relationship
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"
    CUSTOMER = "customer"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    role = Column(String, default="customer")
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    token = Column(String, default=None)
    orders = relationship("Order", back_populates="user",foreign_keys="[Order.user_id]")
