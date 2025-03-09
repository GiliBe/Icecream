from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND
from jinja2 import Template

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user database
fake_users_db = {
    "user": {
        "username": "user",
        "password": "password",  # In production, use hashed passwords!
        "token": "mysecrettoken"
    }
}

# HTML login template
# LOGIN_PAGE = Template("""
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Login</title>
# </head>
# <body>
#     <h2>Login</h2>
#     <form action="/login" method="post">
#         <label>Username:</label>
#         <input type="text" name="username" required><br><br>
#         <label>Password:</label>
#         <input type="password" name="password" required><br><br>
#         <input type="submit" value="Login">
#     </form>
#     {% if error %}
#     <p style="color: red;">{{ error }}</p>
#     {% endif %}
# </body>
# </html>
# """)

@app.get("/")
async def root():
    return {"message": "Hello, world!"}
@app.get("/routes")
async def get_routes():
    return [{"path": route.path, "name": route.name} for route in app.routes]

# @app.get("/", response_class=HTMLResponse)
# async def login_page(request: Request):
#     # return LOGIN_PAGE.render(error=None)
#     return HTMLResponse(content=LOGIN_PAGE.render(error=None))


# @app.post("/login")
# async def login(username: str = Form(...), password: str = Form(...)):
#     user = fake_users_db.get(username)
#     if not user or password != user["password"]:
#         return HTMLResponse(content=LOGIN_PAGE.render(error="Invalid credentials"), status_code=400)

#     response = RedirectResponse(url="/items/", status_code=HTTP_302_FOUND)
#     response.set_cookie(key="access_token", value=user["token"])
#     return response


# @app.get("/items/", response_class=HTMLResponse)
# async def read_items(request: Request, token: str = Depends(oauth2_scheme)):
#     if token != fake_users_db["user"]["token"]:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     return f"<h1>Welcome to Items Page</h1><p>Your token: {token}</p>"

# @app.get("/routes")
# async def list_routes():
#     return app.routes
