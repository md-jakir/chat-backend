import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.models.chatbot import Chatbot
from app.models.knowdegde_base import KnowledgeBase
from app.models.user_chatbot import UserChatbot
from app.schema.UserChatbot import UpdateUserChatbot
from app.db import get_db
from utils.logger import logger
from utils.pdf_utils import process_uploaded_pdfs

router = APIRouter()

@router.get("/")
def get_chatbots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        total = db.query(UserChatbot).count()
        chatbots = db.query(UserChatbot).options(joinedload(UserChatbot.chatbot)).offset(skip).limit(limit).all()

        return {"total": total, "data": chatbots}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/{chatbot_id}")
def get_chatbot(chatbot_id: int, db: Session = Depends(get_db)):
    try:
        chatbot = db.query(UserChatbot).options(joinedload(UserChatbot.chatbot)).filter(UserChatbot.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        return chatbot
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/")
async def create_chatbot(user_id: int, chatbot_id: int, model_id: str, db: Session = Depends(get_db)):
    try:
        user_chatbot = UserChatbot(user_id=user_id, chatbot_id=chatbot_id, model_id = model_id)
        db.add(user_chatbot)
        db.commit()
        db.refresh(user_chatbot)
        return user_chatbot
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.post("/upload-bulk")
async def upload_bulk_user_chatbot(user_ids: List[int] ,chatbot_id: int, model_id: str, db: Session = Depends(get_db)):
    try:
        for user_id in user_ids:
            exists = db.query(UserChatbot).filter_by(user_id=user_id, chatbot_id=chatbot_id, model_id = model_id).first() is not None
            if not exists:
                user_chatbot = UserChatbot(user_id=user_id, chatbot_id=chatbot_id, model_id = model_id)
                db.add(user_chatbot)
        db.commit()
        return {"message": "UserChatbots created successfully"}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.put("/{user_chatbot_id}")
async def update_chatbot(user_chatbot_id: int, body: UpdateUserChatbot, db: Session = Depends(get_db)):
    try:
        user_chatbot = db.query(UserChatbot).filter(UserChatbot.id == user_chatbot_id).first()
        if not user_chatbot:
            raise HTTPException(status_code=404, detail="UserChatbot not found")
        if(body.user_id):
            user_chatbot.user_id = body.user_id
        if(body.chatbot_id):
            user_chatbot.chatbot_id = body.chatbot_id
        if(body.model_id):
            user_chatbot.model_id = body.model_id
        db.commit()
        db.refresh(user_chatbot)
        
        return {
            "status_code": 200,
            "message": "UserChatbot updated successfully",
            "data": user_chatbot
        }
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.delete("/{user_chatbot_id}")
async def delete_chatbot(user_chatbot_id: int, db: Session = Depends(get_db)):
    try:
        user_chatbot = db.query(UserChatbot).filter(UserChatbot.id == user_chatbot_id).first()
        if not user_chatbot:
            raise HTTPException(status_code=404, detail="UserChatbot not found")
        db.delete(user_chatbot)
        db.commit()
        return {
            "status_code": 200,
            "message": "Deleted successfully",
            "data": user_chatbot
        }
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")