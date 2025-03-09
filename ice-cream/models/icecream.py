from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.connection import Base

class IceCream(Base):
    __tablename__ = "icecreams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String)
    stock = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    
    # # Relationship with orders
    orders = relationship("OrderItem", back_populates="icecream")
    order_items = relationship('OrderItem', back_populates='icecream')


    # Relationships
    # order_items = relationship("OrderItem", back_populates="icecream", overlaps="orders")
    # orders = relationship("Order", secondary="order_items", back_populates="icecream")