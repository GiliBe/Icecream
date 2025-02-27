#  Ice Cream Web App - FastAPI Backend Setup

#  Step 1: Project Structure
#  ├── main.py (Entry point)
#  ├── db (Database configurations)
#  │   └── connection.py (PostgreSQL connection)
#  ├── models (Database models)
#  │   ├── user.py
#  │   ├── menu.py
#  │   ├── order.py
#  │   └── material.py
#  └── routers (API routes)
#       ├── user.py
#       ├── menu.py
#       ├── order.py
#       └── material.py

#   Step 2: Setting up FastAPI and connecting to PostgreSQL

#  main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from db.connection import Base, engine
from routers import user, menu, order, material
from sqlalchemy.orm import Session


# Initialize database tables
Base.metadata.create_all(bind=engine)
# user.Base.metadata.create_all(bind=engine)
# menu.Base.metadata.create_all(bind=engine)
# order.Base.metadata.create_all(bind=engine)
# material.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ice Cream Web App")



# Include routers
app.include_router(user.router)
app.include_router(menu.router)
app.include_router(order.router)
app.include_router(material.router)

# Run using: uvicorn main:app --reload

#  Note: Replace 'username' and 'password' with your PostgreSQL credentials.

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Ice Cream Web App!"}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/orders", response_class=HTMLResponse)
async def read_orders(request: Request, db: Session = Depends(SessionLocal)):
    orders = db.query(Order).all()
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})
