from fastapi import HTTPException
from requests import Session
from utils.logger import logger
from ..models.user import User
from ..db import engine, SessionLocal, Base, get_db
from ..schema.user import UserBase
from app.helpers.hash_password import check_password

async def login(db: Session, username: str, password: str):
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not check_password(password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        return user
    
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")