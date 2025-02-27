# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# User schemas
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

# Ice Cream schemas
class IceCreamBase(BaseModel):
    name: str
    description: str
    price: float

class IceCreamCreate(IceCreamBase):
    pass

class IceCream(IceCreamBase):
    id: int
    available: bool

    class Config:
        from_attributes = True

# Order schemas
class OrderItemBase(BaseModel):
    ice_cream_id: int
    quantity: int
    unit_price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: int
    order_date: datetime
    total_amount: float
    status: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    items: List[OrderItem]

    class Config:
        from_attributes = True

# Inventory schemas
class InventoryBase(BaseModel):
    item_name: str
    quantity: float
    unit: str
    reorder_level: float
    supplier_id: int

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int

    class Config:
        from_attributes = True

# Supplier schemas
class SupplierBase(BaseModel):
    name: str
    contact_person: str
    email: str
    phone: str
    address: str

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int
    inventory_items: List[Inventory]

    class Config:
        from_attributes = True