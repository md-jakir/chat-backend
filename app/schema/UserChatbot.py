from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional as optional
from typing import List



class UpdateUserChatbot(BaseModel):
    model_id: optional[str] = None
    user_id: optional[int] = None
    chatbot_id: optional[int] = None