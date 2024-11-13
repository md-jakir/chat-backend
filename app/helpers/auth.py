from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import os

from datetime import datetime, timedelta, timezone

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_SECRET_FOR_VERIFY = os.getenv("JWT_SECRET_FOR_VERIFY")

def create_access_token(data: dict):
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def token_for_verification(data: dict):
    try:
        return jwt.encode(data, JWT_SECRET_FOR_VERIFY, algorithm=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    
def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_FOR_VERIFY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    