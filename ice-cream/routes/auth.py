# routes/auth.py
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.connection import get_db
from models.user import User
import bcrypt
from fastapi import Cookie
from utils import create_access_token,get_current_user
from starlette.status import HTTP_302_FOUND,HTTP_400_BAD_REQUEST
from logger import Logger

logger = Logger(__name__)

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
    logger.info("Register Creation")

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
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
    access_token: str = Cookie(None)
):
    logger.info("Login Creation")

    if access_token:
        logger.info(f"access_token {access_token}")
        try:
            verify_access_token(access_token)  # Validate the token
            return RedirectResponse(url="/items/", status_code=HTTP_302_FOUND)
        except:
            pass  # Invalid or expired token, continue with login

    user = db.query(User).filter(User.email == email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
        request.session["error_message"] = "Incorrect email or password"
        return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)
        
        # return RedirectResponse(
        #     url=f"/login?error=Invalid+credentials", 
        #     status_code=HTTP_302_FOUND
        # )
        
        # return templates.TemplateResponse(
        #     "login.html",  # Your login template name
        #     {"request": request, "error_message": "Incorrect email or password"}
        # )        
        # raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token(data={"sub": user.username})
    user.token = token
    
    db.commit()
    response = RedirectResponse(url="/items/", status_code=HTTP_302_FOUND)
    response.set_cookie(key="access_token", max_age =120, value=token,httponly=True)
    return response

@router.get("/items/", response_class=HTMLResponse)
async def read_items(access_token: str = Cookie(None),db: Session = Depends(get_db),username: str = Depends(get_current_user)):
    print(username)
    print(access_token)
    user = db.query(User).filter(User.token == access_token).first()

    if not access_token or access_token != user.token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return f"<h1>Welcome to Items Page</h1><p>Your token: {access_token} , {username}</p>"
