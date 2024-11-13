from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session 
from typing import List
from pathlib import Path
from app.db import get_db

from sqlalchemy.orm import joinedload
import os

from app.models.session import Session as SessionModel
from app.models.session_hiostory import SessionHistory 

from app.repository.session_history_repository import SessionHistoryRepository

router = APIRouter()

@router.get("/")
def get_sessions(db: Session = Depends(get_db)):
    return db.query(SessionModel).options(joinedload(SessionModel.session_history)).all()

@router.get("/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).options(joinedload(SessionModel.session_history)).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

@router.post("/get_chat_history_by_id")
def get_chat_history(session_id: int, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    chats = db.query(SessionHistory).filter(SessionHistory.session_id == session_id).all()

    if not chats:
        raise HTTPException(status_code=404, detail="Chat not found")

    # chat_history = {i:{"question": chat.qustion, "answer": chat.answer} for i,chat in enumerate(chats)}
    chat_history = SessionHistoryRepository.get_history_json(chats)

    return chat_history

