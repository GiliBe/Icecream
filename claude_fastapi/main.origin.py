# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Request,Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from db.connection import SessionLocal, engine,Base
from schemas import UserCreate, UserResponse,User

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import user
 
# # for postgress
# from database import init_db
# # Initialize database tables
# init_db()

# Initialize FastAPI app
app = FastAPI(title="Ice Cream Shop Management System")
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)

# Create database tables
# models.Base.metadata.create_all(bind=engine)
# user.Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT settings
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

app.include_router(user.router)


# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.get("/", response_class=HTMLResponse,name="index1")
async def read_root(request: Request):
    return templates.TemplateResponse("index1.html", {"request": request})

@app.get("/login", response_class=HTMLResponse,name="login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse,name="register")
async def place_order(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register",response_model=User)
# async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
async def create_user(user: UserCreate= Form(), db: Session = Depends(SessionLocal)):
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
























# Authentication endpoints
# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.email == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password"
#         )
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# User management endpoints
# @app.post("/users/", response_model=User)
# def create_user(user: UserCreate, db: Session = Depends(SessionLocal)):
#     db_user = models.User(
#         email=user.email,
#         hashed_password=get_password_hash(user.password),
#         role=user.role
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @app.get("/users/", response_model=List[User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(SessionLocal)):
#     users = db.query(models.User).offset(skip).limit(limit).all()
#     return users

# # Ice cream management endpoints
# @app.post("/ice-creams/", response_model=schemas.IceCream)
# def create_ice_cream(ice_cream: schemas.IceCreamCreate, db: Session = Depends(get_db)):
#     db_ice_cream = models.IceCream(**ice_cream.dict())
#     db.add(db_ice_cream)
#     db.commit()
#     db.refresh(db_ice_cream)
#     return db_ice_cream

# @app.get("/ice-creams/", response_model=List[schemas.IceCream])
# def read_ice_creams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     ice_creams = db.query(models.IceCream).offset(skip).limit(limit).all()
#     return ice_creams

# # Order management endpoints
# @app.post("/orders/", response_model=schemas.Order)
# def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
#     db_order = models.Order(**order.dict())
#     db.add(db_order)
#     db.commit()
#     db.refresh(db_order)
#     return db_order

# @app.get("/orders/", response_model=List[schemas.Order])
# def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     orders = db.query(models.Order).offset(skip).limit(limit).all()
#     return orders

# # Inventory management endpoints
# @app.post("/inventory/", response_model=schemas.Inventory)
# def create_inventory_item(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
#     db_inventory = models.Inventory(**inventory.dict())
#     db.add(db_inventory)
#     db.commit()
#     db.refresh(db_inventory)
#     return db_inventory

# @app.get("/inventory/", response_model=List[schemas.Inventory])
# def read_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     inventory = db.query(models.Inventory).offset(skip).limit(limit).all()
#     return inventory

# # Supplier management endpoints
# @app.post("/suppliers/", response_model=schemas.Supplier)
# def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
#     db_supplier = models.Supplier(**supplier.dict())
#     db.add(db_supplier)
#     db.commit()
#     db.refresh(db_supplier)
#     return db_supplier

# @app.get("/suppliers/", response_model=List[schemas.Supplier])
# def read_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     suppliers = db.query(models.Supplier).offset(skip).limit(limit).all()
#     return suppliers




# pip install fastapi uvicorn sqlalchemy pydantic python-jose[cryptography] passlib[bcrypt] python-multipart psycopg2-binary
# pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib python-multipart psycopg2-binary
# uvicorn main:app --reload

# ice_cream_shop/
# ├── backend/
# │   ├── app/
# │   │   ├── __init__.py
# │   │   ├── main.py
# │   │   ├── database.py
# │   │   ├── models.py
# │   │   └── schemas.py
# │   ├── requirements.txt
# │   └── alembic/               # For database migrations
# │       ├── versions/
# │       ├── env.py
# │       └── alembic.ini
# ├── frontend/
# │   ├── public/
# │   │   ├── index.html
# │   │   ├── favicon.ico
# │   │   └── assets/
# │   ├── src/
# │   │   ├── components/
# │   │   │   ├── Dashboard/
# │   │   │   │   ├── index.jsx
# │   │   │   │   ├── ProductsView.jsx
# │   │   │   │   ├── OrdersView.jsx
# │   │   │   │   └── ...
# │   │   │   └── Store/
# │   │   │       ├── index.jsx
# │   │   │       ├── ProductCard.jsx
# │   │   │       └── Cart.jsx
# │   │   ├── pages/
# │   │   │   ├── Admin.jsx
# │   │   │   ├── Store.jsx
# │   │   │   └── Login.jsx
# │   │   ├── services/
# │   │   │   └── api.js
# │   │   ├── utils/
# │   │   │   └── helpers.js
# │   │   ├── App.jsx
# │   │   └── index.jsx
# │   ├── package.json
# │   └── vite.config.js
# ├── docker/
# │   ├── Dockerfile.backend
# │   ├── Dockerfile.frontend
# │   └── docker-compose.yml
# └── README.md