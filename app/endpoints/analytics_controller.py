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
from app.schema.chatbot import ChatbotResponse, UpdateChatbotBase, QueryInput, FeedBack

from app.db import get_db
from utils import set_user_feedback
from utils.logger import logger
from utils.pdf_qna import upload_pdf_chain_call
from utils.pdf_utils import process_uploaded_pdfs
from utils.sample_q import  get_sample_questions

from app.repository.analytics_repository import AnalyticsRepository


# sessions = {}

router = APIRouter()


@router.get("/")
def get_analytics_data(db: Session = Depends(get_db)):
    try:
    
        
        # Execute synchronous functions sequentially
        session_message_counts = AnalyticsRepository.get_session_message_counts(db)
        message_volume = AnalyticsRepository.get_message_volume(db)
        sessions_per_user = AnalyticsRepository.get_sessions_per_user(db)
        avg_response_time = AnalyticsRepository.get_avg_response_time(db)
        message_count_per_month = AnalyticsRepository.get_message_count_per_month(db)
        message_count_per_hour = AnalyticsRepository.get_message_count_per_hour(db)
        average_messages_per_session = AnalyticsRepository.get_average_messages_per_session(db)
        total_unique_user_count = AnalyticsRepository.get_total_unique_user_count(db)
        user_retention_rate = AnalyticsRepository.calculate_user_retention(db)
        user_creation_stats_per_month = AnalyticsRepository.get_user_creation_stats_per_month(db)
        feedback_counts = AnalyticsRepository.get_feedback_counts(db)

        # Format the results into a JSON-compatible dictionary
        analytics_data = {
            "session_message_counts": session_message_counts,
            "message_volume": message_volume,
            "sessions_per_user": sessions_per_user,
            "avg_response_time": avg_response_time,
            "message_count_per_month": message_count_per_month,
            "message_count_per_hour": message_count_per_hour,
            "average_messages_per_session": average_messages_per_session,
            "total_unique_user_count": total_unique_user_count,
            "user_retention_rate": user_retention_rate,
            "user_creation_stats_per_month": user_creation_stats_per_month,
            "feedback_counts": feedback_counts,
        }
        
        return analytics_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_session_message_counts")
async def get_analytics(db: Session = Depends(get_db)):
    val=AnalyticsRepository.get_session_message_counts(db)
    return val

# @router.get("/average_message_per_session")
# async def get_average_message_per_session(db: Session = Depends(get_db)):
#     val=AnalyticsRepository.get_average_messages_per_session(db)
#     return val

# @router.get("/total_unique_user_count")
# async def get_total_unique_user_count(db: Session = Depends(get_db)):
#     val=AnalyticsRepository.get_total_unique_user_count(db)
#     return val

# @router.get("/get_user_retenion_rate")
# async def get_user_retenion_rate(db: Session = Depends(get_db)):
#     val=AnalyticsRepository.calculate_user_retention(db)
#     return val

# @router.get("/get_user_created_per_month")
# async def get_user_created_per_month(db: Session = Depends(get_db)):
#     val=AnalyticsRepository.get_user_creation_stats_per_month(db)
#     return val

# @router.get("/get_feedback_stats")
# async def get_feedback_stats(db: Session = Depends(get_db)):
#     val=AnalyticsRepository.get_feedback_counts(db)
#     return val


# @router.get("/message_volume")
# async def get_message_volume(db: Session = Depends(get_db)):
#     val=AnalyticsRepository.get_message_volume(db)
#     return val

# @router.get("/sessions_per_user")
# async def get_sessions_per_user(db: Session = Depends(get_db)):
#     val=AnalyticsRepository.get_sessions_per_user(db)
#     return val

# @router.get("/response_time_per_chatbot")
# async def get_avg_response_time(db: Session = Depends(get_db)):
#     val=AnalyticsRepository.get_avg_response_time(db)
#     return val

# @router.get("/message_count_per_month")
# async def get_message_count_per_month(db: Session = Depends(get_db)):
#     val=AnalyticsRepository.get_message_count_per_month(db)
#     return val

# @router.get("/message_count_per_hour")
# async def get_message_count_per_hour(db: Session = Depends(get_db)):
#     val=AnalyticsRepository.get_message_count_per_hour(db)
#     return val

# @router.get("/message_volume")
# async def get_message_volume(db: Session = Depends(get_db)):
#     val=AnalyticsRepository.get_message_volume(db)
#     return val
