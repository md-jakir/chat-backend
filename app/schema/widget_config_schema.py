from pydantic import BaseModel
from datetime import datetime

class WidgetConfig(BaseModel):
    id: int
    name: str
    message_alignment: str
    bubble_shadow: str
    bubble_border: bool
    text_color: str
    text_shade: int
    bubble_color: str
    bubble_shade: int
    header_color: str
    header_shade: int

class WidgetConfigCreate(BaseModel):
    name: str
    message_alignment: str
    bubble_shadow: str
    bubble_border: bool
    text_color: str
    text_shade: int
    bubble_color: str
    bubble_shade: int
    header_color: str
    header_shade: int
    voice_chat_option: bool
    feedback_option: bool
    chat_history_option: bool


    class Config:
        orm_mode = True
        