# routes/order.py
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.connection import get_db
from models.order import  Order, OrderItem
from models.icecream import IceCream
from typing import List
from utils import get_current_user
from logger import Logger

logger = Logger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/add-to-cart")
async def add_to_cart(
    request: Request,
    icecream_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    logger.info("Add To Cart")
    logger.info(f"session {request.session}")
    logger.info(f"quantity {quantity}")
    # In a real app, you'd use sessions for the cart
    # For now, we'll redirect back to menu with a message
    session = request.session
    cart = session.get("cart", {})

    # Fetch ice cream details from the database
    icecream = db.query(IceCream).filter(IceCream.id == icecream_id).first()
    if not icecream:
        return RedirectResponse(url="/menu", status_code=303)

    # Update cart
    if icecream_id in cart:
        cart[icecream_id]["quantity"] += quantity  # Update quantity if exists
    else:
        cart[icecream_id] = {
            "id": icecream.id,
            "name": icecream.name,
            "image_url": icecream.image_url,
            "price": icecream.price,
            "quantity": quantity,
        }

    session["cart"] = cart  # Save back to session
    # session.modified = True  # Mark session as changed

    return RedirectResponse(url="/", status_code=303)

@router.get("/cart", name ='cart')
async def view_cart(request: Request):
    logger.info("Cart Page")

    session = request.session
    logger.info(session)
    cart = session.get("cart", {})
    logger.info("Cart 3 Page")

    cart_items = [
        {
            "icecream_id": icecream_id,  # Store the icecream_id
            "icecream": {
                "name": item["name"],
                "image_url": item["image_url"],
                "price": item["price"],
            },
            "quantity": item["quantity"],
        }
        for icecream_id, item in cart.items()
    ]

    total_price = sum(item["quantity"] * item["icecream"]["price"] for item in cart_items)

    return templates.TemplateResponse(
        "cart.html",
        {"request": request, "cart_items": cart_items, "total_price": total_price}
    )

@router.post("/update-cart/{icecream_id}")
async def update_cart(request: Request, icecream_id: int, quantity: int = Form(...)):
    logger.info("Cart Update Page")

    session = request.session
    cart = session.get("cart", {})
    print(icecream_id)
    print(cart)
    
    if str(icecream_id) in cart:
        cart[str(icecream_id)]["quantity"] = quantity  # Update quantity if exists

    
    session["cart"] = cart
    # session.modified = True

    return RedirectResponse(url="/cart", status_code=303)

@router.post("/remove-from-cart/{icecream_id}")
async def remove_from_cart(icecream_id: int, request: Request):
    logger.info("Cart Remove Page")
    
    session = request.session
    cart = session.get("cart", {})

    # if icecream_id in cart:
    #     del cart[icecream_id]

    if str(icecream_id) in cart:  # Ensure icecream_id is a string (session keys are strings)
        del cart[str(icecream_id)]  # Remove item from cart
    session["cart"] = cart
    # session.modified = True

    return RedirectResponse(url="/cart", status_code=303)

@router.post("/checkout")
async def checkout(
    request: Request,
    customer_name: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info("Checkout Page")

    session = request.session
    cart = session.get("cart", {})
    print(cart)

    if not cart:
        return RedirectResponse(url="/cart", status_code=303)

    # Calculate total price
    total_price = sum(item["quantity"] * item["price"] for item in cart.values())

    # Create Order in the database
    new_order = Order(user_id=customer_name, total_amount=total_price)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Add each cart item as an OrderItem
    # for item in cart.values():
            # print(item)

    for k,v  in cart.items():
        print(k)
        print(v)
        order_item = OrderItem(
            order_id=new_order.id,
            icecream_id=k,
            icecream_name=v["name"],
            quantity=v["quantity"],
            unit_price=v["price"]
        )
        db.add(order_item)

    db.commit()

    # Clear the cart after successful checkout
    session["cart"] = {}
    # session.modified = True

    return RedirectResponse(url=f"/order_confirmation/{new_order.id}", status_code=303)

@router.post("/place-order")
async def place_order(
    request: Request,
    db: Session = Depends(get_db)
):
    # Get cart items from session
    # Create order and order items
    # Clear cart
    # Redirect to order confirmation
    return RedirectResponse(url="/order-confirmation", status_code=303)

@router.get("/my-orders")
async def my_orders(
    request: Request,
    db: Session = Depends(get_db)
):
    # Get user's orders
    # In a real app, you'd get the user_id from the session
    user_id = 1  # Placeholder
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return templates.TemplateResponse(
        "my_orders.html",
        {"request": request, "orders": orders}
    )