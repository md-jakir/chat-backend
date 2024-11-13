from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path

from sqlalchemy.orm import joinedload
import os

from app.models.chatbot import Chatbot
from app.models.knowdegde_base import KnowledgeBase
from app.models.sample_qustion import SampleQustion
from app.models.user import User

from app.schema.chatbot import ChatbotResponse, UpdateKnowdelgebase, UpdateChatbotBase, QueryInput, FeedBack

from app.db import get_db
from utils import set_user_feedback
from utils.logger import logger
from utils.pdf_qna import upload_pdf_chain_call
from utils.pdf_utils import process_uploaded_pdfs
from utils.sample_q import  get_sample_questions

router = APIRouter()

@router.put("/{knowledge_base_id}/active_status")
def update_knowledge_base_status(knowledge_base_id: int, active_status: bool, db: Session = Depends(get_db)):
    knowledge_base = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not knowledge_base:
        raise HTTPException(status_code=404, detail="Knowledge Base not found")
    knowledge_base.active_status = active_status
    db.commit()
    return {"message": "Knowledge Base status updated successfully"}


@router.delete("/{knowledge_base_id}")
def delete_knowledge_base(knowledge_base_id: int, db: Session = Depends(get_db)):
    knowledge_base = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_base_id).first()
    if not knowledge_base:
        raise HTTPException(status_code=404, detail="Knowledge Base not found")
    db.delete(knowledge_base)
    db.commit()
    return {"message": "Knowledge Base deleted successfully"}