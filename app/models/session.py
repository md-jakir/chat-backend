from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.db import Base
from sqlalchemy.orm import relationship
from .session_hiostory import SessionHistory

class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name= Column(String(255))
    token = Column(String(255), nullable=False)
    chatbot_id = Column(Integer, ForeignKey('chatbot.id'), default=None)
    chatbot = relationship("Chatbot", back_populates="session")
    user_id = Column(Integer, nullable=True, default=None)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    # model_id = Column(String(255))
    


    session_history = relationship("SessionHistory", back_populates="session")