# models/user.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from db.connection import Base
from datetime import datetime


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    customer_name = Column(String, ForeignKey("users.username"))
    total_amount = Column(Float)
    date_ordered = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # "pending", "completed", "cancelled"
    
    # Relationships
    # user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    user = relationship("User", back_populates="orders", foreign_keys=[user_id])
    customer = relationship("User", foreign_keys=[customer_name])  # Separate relationship

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    icecream_id = Column(Integer, ForeignKey("icecreams.id"))
    icecream_name = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    icecream = relationship('IceCream', back_populates='order_items')
