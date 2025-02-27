# Directory Structure:
# /icecream_app
#   ├── main.py
#   ├── /routes
#   │   ├── __init__.py
#   │   ├── auth.py
#   │   └── base.py
#   ├── /static
#   │   └── styles.css
#   ├── /templates
#   │   ├── login.html
#   │   └── register.html
#   ├── /schemas
#   │   └── user.py
#   ├── /models
#   │   └── user.py
#   └── /database
#       └── db.py

# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import auth, base
from database.db import engine
from models.user import Base

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(base.router)
app.include_router(auth.router)

# Create database tables
Base.metadata.create_all(bind=engine)

# routes/__init__.py
# Empty file to make the directory a Python package

# routes/base.py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# routes/auth.py
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import User
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/register")
async def register(
    request: Request,
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
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    
    return RedirectResponse(url="/", status_code=303)

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
    
    return {"message": "Login successful"}

# schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

# models/user.py
from sqlalchemy import Column, Integer, String
from database.db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# database/db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./icecream.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # static/styles.css
# body {
#     font-family: Arial, sans-serif;
#     max-width: 800px;
#     margin: 0 auto;
#     padding: 20px;
#     background-color: #f5f5f5;
# }

# .form-container {
#     background: white;
#     padding: 20px;
#     border-radius: 8px;
#     box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
# }

# .form-group {
#     margin-bottom: 15px;
# }

# input[type="email"],
# input[type="password"] {
#     width: 100%;
#     padding: 8px;
#     margin-top: 5px;
#     border: 1px solid #ddd;
#     border-radius: 4px;
# }

# button {
#     background-color: #4CAF50;
#     color: white;
#     padding: 10px 15px;
#     border: none;
#     border-radius: 4px;
#     cursor: pointer;
# }

# button:hover {
#     background-color: #45a049;
# }

# .error {
#     color: red;
#     margin-top: 5px;
# }

# # static/styles.css
# body {
#     font-family: Arial, sans-serif;
#     max-width: 800px;
#     margin: 0 auto;
#     padding: 20px;
#     background-color: #f5f5f5;
# }

# .form-container {
#     background: white;
#     padding: 20px;
#     border-radius: 8px;
#     box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
# }

# .form-group {
#     margin-bottom: 15px;
# }

# input[type="email"],
# input[type="password"] {
#     width: 100%;
#     padding: 8px;
#     margin-top: 5px;
#     border: 1px solid #ddd;
#     border-radius: 4px;
# }

# button {
#     background-color: #4CAF50;
#     color: white;
#     padding: 10px 15px;
#     border: none;
#     border-radius: 4px;
#     cursor: pointer;
# }

# button:hover {
#     background-color: #45a049;
# }

# .error {
#     color: red;
#     margin-top: 5px;
# }

# <!-- templates/login.html -->
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Login - Ice Cream Shop</title>
#     <link rel="stylesheet" href="{{ url_for('static', path='/styles.css') }}">
# </head>
# <body>
#     <div class="form-container">
#         <h2>Login</h2>
#         <form action="/login" method="POST">
#             <div class="form-group">
#                 <label for="email">Email:</label>
#                 <input type="email" id="email" name="email" required>
#             </div>
#             <div class="form-group">
#                 <label for="password">Password:</label>
#                 <input type="password" id="password" name="password" required>
#             </div>
#             <button type="submit">Login</button>
#         </form>
#         <p>Don't have an account? <a href="/register">Register here</a></p>
#     </div>
# </body>
# </html>

# <!-- templates/register.html -->
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Register - Ice Cream Shop</title>
#     <link rel="stylesheet" href="{{ url_for('static', path='/styles.css') }}">
# </head>
# <body>
#     <div class="form-container">
#         <h2>Register</h2>
#         <form action="/register" method="POST">
#             <div class="form-group">
#                 <label for="email">Email:</label>
#                 <input type="email" id="email" name="email" required>
#             </div>
#             <div class="form-group">
#                 <label for="password">Password:</label>
#                 <input type="password" id="password" name="password" required>
#             </div>
#             <button type="submit">Register</button>
#         </form>
#         <p>Already have an account? <a href="/">Login here</a></p>
#     </div>
# </body>
# </html>