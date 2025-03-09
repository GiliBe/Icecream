# routes/menu.py
from fastapi import APIRouter, Request, Depends, HTTPException, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.connection import get_db
from models.icecream import IceCream
from models.order import  Order, OrderItem
from typing import List
import shutil
import os
from logger import Logger

logger = Logger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/menu")
async def menu_page(request: Request, db: Session = Depends(get_db)):
    logger.info("Menu Page")
    icecreams = db.query(IceCream).filter(IceCream.is_available == True).all()
    return templates.TemplateResponse(
        "menu.html",
        {"request": request, "icecreams": icecreams}
    )

# @router.get("/admin/menu")
# async def admin_menu(request: Request, db: Session = Depends(get_db)):
#     logger.info("Admin Menu Page")

#     icecreams = db.query(IceCream).all()
#     return templates.TemplateResponse(
#         "admin/menu_management.html",
#         {"request": request, "icecreams": icecreams}
#     )

# @router.post("/admin/icecream")
# async def create_icecream(
#     request: Request,
#     name: str = Form(...),
#     description: str = Form(...),
#     price: float = Form(...),
#     image: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     logger.info("Admin Icereams Page")

#     # Save image
#     # image_path = f"static/images/{image.filename}"
#     # with open(image_path, "wb") as buffer:
#     #     shutil.copyfileobj(image.file, buffer)
#     image_path= None

#     # Create ice cream
#     new_icecream = IceCream(
#         name=name,
#         description=description,
#         price=price,
#         image_url=image_path
#     )
#     db.add(new_icecream)
#     db.commit()
    
#     return {"success": True, "id": new_icecream.id}

# @router.post("/admin/icecream/{icecream_id}")
# async def update_icecream(
#     icecream_id: int,
#     name: str = Form(...),
#     description: str = Form(...),
#     price: float = Form(...),
#     is_available: bool = Form(...),
#     db: Session = Depends(get_db)
# ):
#     logger.info("Admin Iceream Page")
#     icecream = db.query(IceCream).filter(IceCream.id == icecream_id).first()
#     if not icecream:
#         raise HTTPException(status_code=404, detail="Ice cream not found")
    
#     icecream.name = name
#     icecream.description = description
#     icecream.price = price
#     icecream.is_available = is_available
    
#     db.commit()
#     return {"success": True}
