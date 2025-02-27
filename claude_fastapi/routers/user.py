# routers/user.py
from fastapi import APIRouter, Depends, HTTPException,Form
from sqlalchemy.orm import Session
from db.connection import SessionLocal
from models import User
from schemas import UserCreate, UserResponse
from typing import List

router = APIRouter(prefix="/users")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/register", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# @router.post("/register", response_model=UserResponse)
# async def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = User(username=user.username, email=user.email, password=user.password)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

# @app.get("/register", response_class=HTMLResponse,name="register")
# async def place_order(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register",response_model=User)
# async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
async def create_user(user: UserCreate= Form(), db: Session = Depends(get_db())):
    print(user)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password
        # hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # return templates.TemplateResponse("register.html", {"request": request})
    
    return db_user



