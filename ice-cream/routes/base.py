# routes/base.py
from fastapi import APIRouter, Request ,Depends,Response,Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from utils import get_current_user,check_if_logged
from db.connection import get_db
from models.icecream import IceCream
from logger import Logger
from sqlalchemy.orm import Session

logger = Logger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, access_token: str = Cookie(None),username: str = Depends(get_current_user), logged: bool = Depends(check_if_logged),db: Session = Depends(get_db)):
    logger.info("Home Page")
    logger.info(username)
    logger.info(logged)
    # if not logged:
    #     return RedirectResponse(url="/login", status_code=302)        
    # if access_token:
    #     try:
    #         logger.info("Redirect to items")
    #         return RedirectResponse(url="/items/", status_code=302)
    #     except:
    #         logger.info("Redirect to Login")
    #         return RedirectResponse(url="/login", status_code=302)
    #         pass  # Invalid or expired token, show login page
    # logger.info("Redirect to index")
    icecreams = db.query(IceCream).filter(IceCream.is_available == True).all()
    session = request.session
    logger.info(f'session {session}')
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "icecreams": icecreams}
    )

    # return templates.TemplateResponse("menu.html", {"request": request})
    # return logged

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    logger.info("Register Page")
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/register_success", response_class=HTMLResponse)
async def register_success(request: Request):
    logger.info("Register Success Page")
    return templates.TemplateResponse("register_success.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, access_token: str = Cookie(None)):
    logger.info("Login Page")
    if access_token != None:
        try:
            return RedirectResponse(url="/items/", status_code=302)
        except:
            pass  # Invalid or expired token, show login page
    error_message = request.session.pop("error_message", None)

    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "error_message": error_message}
    )

    # return templates.TemplateResponse("login.html", {"request": request})

@router.get("/login_success", response_class=HTMLResponse)
async def register_success(request: Request):
    logger.info("Login Success Page")
    return templates.TemplateResponse("login_success.html", {"request": request})

@router.get("/logout")
async def logout(request: Request,response: Response,access_token: str = Cookie(None)):
    logger.info("Logout Page")
    request.session.clear()  
    if access_token:
        try:
            response = RedirectResponse(url="/", status_code=302)
            response.delete_cookie("access_token")
        except:
            pass  # Invalid or expired token, show login page

    return response
