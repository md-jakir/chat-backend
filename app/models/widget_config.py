from sqlalchemy import Column, Integer, String,  DateTime, func, Boolean, Enum
from app.db import Base
from sqlalchemy.orm import relationship
from .session import Session
import enum


class AlignmentEnum(enum.Enum):
    vertical = 'vertical'
    horizontal = 'horizontal'

class ShadowEnum(enum.Enum):
    outer = 'outer'
    inner = 'inner'
    none = 'none'

class WidgetConfig(Base):
    __tablename__ = 'widget_config'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    message_alignment = Column(Enum(AlignmentEnum), nullable=False, default=AlignmentEnum.vertical) 
    bubble_shadow = Column(Enum(ShadowEnum), nullable=False, default=ShadowEnum.outer)
    bubble_border = Column(Boolean, nullable=False, default=False)
    text_color = Column(String(255), nullable=False, default='#000000')
    text_shade = Column(Integer, nullable=False, default=700)
    bubble_color = Column(String(255), nullable=False, default='#ffffff')
    bubble_shade = Column(Integer, nullable=False, default=500)
    header_color = Column(String(255), nullable=False, default='#ffffff')
    header_shade = Column(Integer, nullable=False, default=500)
    voice_chat_option = Column(Boolean, nullable=False, default=True)
    feedback_option = Column(Boolean, nullable=False, default=False)
    chat_history_option = Column(Boolean, nullable=False, default=False)


    
    