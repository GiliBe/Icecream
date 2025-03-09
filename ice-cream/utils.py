from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import Depends, Cookie, HTTPException, status,Response
from fastapi.responses import RedirectResponse
from logger import Logger

logger = Logger(__name__)

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"  # Hashing algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expires in 30 minutes


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # Add expiration time
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# def check_if_logged():

def get_current_user(access_token: str = Cookie(None)):
    logger.info("get_current_user")    
    if not access_token:
        return None
    else:
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            logger.info(f'Current User - {payload.get("sub")}')
            return payload.get("sub")
        except:
            logger.info("No Current User")
            return None  # Redirect on invalid token

def check_if_logged(access_token: str = Cookie(None)):
    logger.info("check_if_logged")
    if not access_token:
        logger.info("Redirect to login")
        logged = False
        return logged  
        # return RedirectResponse(url="/login", status_code=303)  # Redirect to login
    else:
        logged = True
        logger.info("invalid token")
        # return RedirectResponse(url="/", status_code=303)  # Redirect on invalid token
        return logged  

