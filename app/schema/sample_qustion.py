from pydantic import BaseModel, EmailStr
from datetime import datetime

class SampleQuestionBase(BaseModel):
    text: str
    chatbot_id: int

class SampleQuestionCreate(SampleQuestionBase):
    pass

class SampleQuestionResponse(BaseModel):
    id: int
    text: str
    chatbot_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True