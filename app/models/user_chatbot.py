from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from app.db import Base
from passlib.hash import bcrypt
from sqlalchemy.orm import relationship

class UserChatbot(Base):
    __tablename__ = 'user_chatbot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True, default=None)
    chatbot_id = Column(Integer, ForeignKey('chatbot.id'), nullable=True, default=None)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    model_id = Column(String(255))
    
    user = relationship('User', back_populates='user_chatbot')
    chatbot = relationship('Chatbot', back_populates='user_chatbot')