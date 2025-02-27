from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import SessionLocal
from models.material import Material
from schemas.material import MaterialCreate, MaterialResponse
from typing import List

router = APIRouter(prefix="/materials")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[MaterialResponse])
async def get_materials(db: Session = Depends(get_db)):
    return db.query(Material).all()

@router.post("/")
async def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    db.add(material)
    db.commit()
    db.refresh(material)
    return material
