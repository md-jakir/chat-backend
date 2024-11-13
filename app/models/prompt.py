from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.db import Base
from sqlalchemy.orm import relationship

class Prompt(Base):
    __tablename__ = 'prompt'
    prompt_id = Column(Integer, primary_key=True, autoincrement=True)
    prompt_text = Column(String(65535), nullable=True)
    chatbot_id = Column(Integer, ForeignKey('chatbot.id'), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    chatbot = relationship('Chatbot', back_populates='prompt')
