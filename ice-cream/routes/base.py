# routes/base.py
from fastapi import APIRouter, Request ,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse,name="index")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/register_success", response_class=HTMLResponse)
async def register_success(request: Request):
    return templates.TemplateResponse("register_success.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/login_success", response_class=HTMLResponse)
async def register_success(request: Request):
    return templates.TemplateResponse("login_success.html", {"request": request})
