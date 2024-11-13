from pydantic import BaseModel, EmailStr
from fastapi import Form
from datetime import datetime
from app.schema.user import UserResponse
from app.schema.knowledge_base import KnowledgeBaseResponse
from typing import Optional, List

class ChatbotBase(BaseModel):
    name: str
    gretting_message: str
    user_id: int
    active_status: bool

class UpdateChatbotBase(BaseModel):
    name: Optional[str] = None
    gretting_message: Optional[str] = None
    active_status: Optional[bool] = None

class ChatbotResponse(BaseModel):
    id: int
    name: str
    gretting_message: str
    active_status: bool
    created_at: datetime
    updated_at: datetime
    user: Optional[UserResponse]
    # knowledge_base: Optional[List[KnowledgeBaseResponse]]

class GetAllChatbotResponse(BaseModel):
    total: int
    data: List[ChatbotResponse]
    
class QueryInput(BaseModel):
    question: str
    # session_id: str
    chatbot_id: str
    token: str
    user_id: int

class FeedBack(BaseModel):
    session_id: str
    query_id: int
    user_feedback: bool
    text_feedback: str

class UpdateKnowdelgebase(BaseModel):
    id: int = Form(...)
    path: Optional[str] = Form(...)
    uploadFile: Optional[bytes] = Form(...)


    # class SimpleModel(BaseModel):
    # no: int = Form(...)
    # nm: str = Form(...)
    # f: UploadFile = Form(...)

class Chatbot(ChatbotBase):
    id: int

    class Config:
        from_attributes = True
    


class AWSQueryInput(BaseModel):
    question: str
    # session_id: str
    chatbot_id: str
    token: str
    model_id: str 

class PromptBase(BaseModel):
    prompt: str