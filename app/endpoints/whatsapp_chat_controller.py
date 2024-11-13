from fastapi import APIRouter, Form, Depends, HTTPException, UploadFile, File, Body, status
from twilio.rest import Client
from app.db import get_db
from sqlalchemy.orm import Session
import re
import json

from utils.logger import logger

from redis.asyncio import Redis
from app.config.redis import get_redis
 
from typing import Optional
from app.models.user import User
from app.models.user_chatbot import UserChatbot
from app.repository.session_repository import SessionRepository

from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from utils.pdf_qna import upload_pdf_chain_call_whatsapp

router = APIRouter()

@router.get("/", response_class=PlainTextResponse)
async def whatsapp_callback():
    print("ok")
    return "ok"

@router.post("/", response_class=PlainTextResponse)
async def send_message(Body: Optional[str] = Form(None), From: Optional[str] = Form(None), db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):    
    try:
        cashed_chatbot = await redis.get(From)
 
        response_message = ""

        if Body is None:
            response_message = "Please provide the message."
        elif "#chatbot" in Body.lower():
            chatbot_id = Body.split(":")[1].strip()
            await redis.set(From, f"{chatbot_id}")

            response_message = "Chatbot updated successfully. You can now send messages to your Chatbot."

        elif cashed_chatbot is not None:
            response_message = Body
            cashed_toke = await redis.get(f"{From}-session-token")
            if cashed_toke is None:
                
                session_id=SessionRepository.create_or_update_session(db,f"{From}-session-token", cashed_chatbot, f"{From}-session-token")

                await redis.set(f"{From}-session-token", f"{session_id}")
            else:
                session_id = cashed_toke
        
                
            ans= await upload_pdf_chain_call_whatsapp(session_id, Body, cashed_chatbot, db)
                
            
            response_message = ans
        else:
            if "#chatbot" in Body.lower():
                chatbot_id = Body.split(":")[1].strip()
        
                await redis.set(From, f"{chatbot_id}")

                response_message = "Successfully connected to your Chatbot. You can now send messages to your Chatbot." 
                
            else:
                response_message = "Please provide the chatbot ID.\nFor example, you can reply with:\n#Chatbot: 12\n\nOr change your chatbot by replying with:\nUpdate #Chatbot: 15"
        

        

        return response_message
    
    except Exception as e:
        logger.exception(e)
        return "An error occurred. Please try again later."
