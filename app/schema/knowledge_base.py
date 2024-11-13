from pydantic import BaseModel, EmailStr
from datetime import datetime

class KnowledgeBase(BaseModel):
    path: str
    chatbot_id: int
    id: int
    active_status: bool
    created_at: datetime
    updated_at: datetime


class KnowledgeBaseResponse(BaseModel):
    path: str
    active_status: bool
    created_at: datetime
    chatbot_id: int
    id: int
    updated_at: datetime


    class Config:
        from_attributes = True
