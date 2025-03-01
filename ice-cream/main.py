# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import auth, base,order,menu,admin
from db.connection import engine
from models.user import Base
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
SECRET_KEY = "your_super_secret_key"
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, session_cookie="session")


# Include routers
app.include_router(base.router)
app.include_router(auth.router)
app.include_router(order.router)
app.include_router(menu.router)
app.include_router(admin.router)

# Create database tables
Base.metadata.create_all(bind=engine)
