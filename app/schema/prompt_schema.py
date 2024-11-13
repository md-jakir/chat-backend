from pydantic import BaseModel
from datetime import datetime

class Prompt(BaseModel):
    prompt_id: int
    prompt_text: str
    chatbot_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True