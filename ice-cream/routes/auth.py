# routes/auth.py
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.connection import get_db
from models.user import User
import bcrypt


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if user exists
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user
    user = User(username=username,email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    
    return RedirectResponse(url="/register_success", status_code=303)

@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return RedirectResponse(url="/login_success", status_code=303)
    
    return {"message": "Login successful"}