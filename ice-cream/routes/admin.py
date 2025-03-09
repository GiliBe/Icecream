# routes/base.py
from fastapi import APIRouter, Request, Depends, HTTPException, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.connection import get_db
from models.icecream import IceCream
from models.user import User
from models.order import  Order, OrderItem
from models.icecream import IceCream
from typing import List
import shutil
import os
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin/users", name = 'admin/users')
async def get_all_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()

    return templates.TemplateResponse("admin/users_managment.html", {"request": request, "users": users})

@router.get("/admin/menu", name = 'admin/menu')
async def admin_menu(request: Request, db: Session = Depends(get_db)):
    icecreams = db.query(IceCream).all()
    return templates.TemplateResponse(
        "admin/menu_management.html",
        {"request": request, "icecreams": icecreams}
    )

@router.get("/admin/dashboard", name = 'admin/dashboard')
async def get_all_users(request: Request, db: Session = Depends(get_db)):

    orders = db.query(Order).all()
    icecreams = db.query(IceCream).all()
    users = db.query(User).all()
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {"request": request, "orders": orders, "icecreams": icecreams, "users": users})
    
    # return render_template('admin/dashboard.html', orders=orders, ice_creams=ice_creams, users=users)

@router.get("/gili")
async def home(request: Request):
    return templates.TemplateResponse("gili.html", {"request": request})

@router.post("/admin/user")
async def create_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    role: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    # Check if user exists
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create user
    user = User(username=username,email=email, hashed_password=hashed_password,role=role)
    
    if role == "admin":
        user.is_admin = True

    db.add(user)
    db.commit()
    
    return {"success": True, "id": user.id}

@router.post("/admin/inventory/icecream/edit/{icecream_id}")
async def edit_icecream_inventory(
    request: Request, icecream_id: int, 
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    image: UploadFile = File(...),


):
    logger.info("edit_icecream_inventory")
    new_icecream_inventory = db.query(IceCream).filter(IceCream.id == icecream_id).first()




    return RedirectResponse(url="/admin/dashboard.html", status_code=303)


















@router.post("/admin/icecream/inventory/create_icecream", name = "admin/icecream/inventory/create_icecream")
async def create_icecream(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save image
    # image_path = f"static/images/{image.filename}"
    # with open(image_path, "wb") as buffer:
    #     shutil.copyfileobj(image.file, buffer)
    image_path= None
    # Check if Icecream exists
    if db.query(IceCream).filter(IceCream.name == name).first():
        raise HTTPException(status_code=400, detail="IceCream already exsist")

    # Create ice cream
    new_icecream = IceCream(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_url=image_path
    )
    db.add(new_icecream)
    db.commit()
    
    return {"success": True, "id": new_icecream.id}

@router.post("/admin/icecream/{icecream_id}")
async def update_icecream(
    icecream_id: int,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    is_available: bool = Form(...),
    db: Session = Depends(get_db)
):
    icecream = db.query(IceCream).filter(IceCream.id == icecream_id).first()
    if not icecream:
        raise HTTPException(status_code=404, detail="Ice cream not found")
    
    icecream.name = name
    icecream.description = description
    icecream.price = price
    icecream.is_available = is_available
    
    db.commit()
    return {"success": True}
