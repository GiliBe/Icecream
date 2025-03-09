# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import auth, base,order,menu,admin
from db.connection import engine
from models.user import Base
from logger import Logger
from starlette.middleware.sessions import SessionMiddleware

logger = Logger(__name__)
logger.info("Starting App...")
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")  # Change this secret key
app.mount("/static", StaticFiles(directory="static"), name="static")


# Include routers
app.include_router(base.router)
app.include_router(auth.router)
app.include_router(order.router)
app.include_router(menu.router)
app.include_router(admin.router)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/routes")
async def get_routes():
    return [{"path": route.path, "name": route.name} for route in app.routes]

