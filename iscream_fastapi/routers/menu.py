# routers/menu.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import SessionLocal
from models.menu import MenuItem
from schemas.menu import MenuResponse
from typing import List

router = APIRouter(prefix="/menu")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[MenuResponse])
async def get_menu_items(db: Session = Depends(get_db)):
    return db.query(MenuItem).all()

@router.post("/", response_model=MenuResponse)
async def create_menu_item(item: MenuResponse, db: Session = Depends(get_db)):
    db_menu_item = MenuItem(item_name=item.name, description=item.description, price=item.price, image_url=item.image_url)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
