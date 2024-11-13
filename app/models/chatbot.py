from sqlalchemy import Column, Integer, String,  DateTime, func, Boolean
from app.db import Base
from sqlalchemy.orm import relationship
from .session import Session

class Chatbot(Base):
    __tablename__ = 'chatbot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    gretting_message = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    knowledge_base_path = Column(String(255), nullable=True, default=None)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    active_status = Column(Boolean, default=True, nullable=False)

    user_chatbot = relationship('UserChatbot', back_populates='chatbot')
    knowledge_base = relationship("KnowledgeBase", back_populates="chatbot")
    sample_qustion = relationship("SampleQustion", back_populates="chatbot")
    session = relationship("Session", back_populates="chatbot")
    prompt = relationship('Prompt', back_populates='chatbot', uselist=False)  # One-to-One relationship
    