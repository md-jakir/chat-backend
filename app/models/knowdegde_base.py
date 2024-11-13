from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from app.db import Base
from sqlalchemy.orm import relationship

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(255), nullable=False)
    chatbot_id = Column(Integer, ForeignKey('chatbot.id'), default=None)
    chatbot = relationship("Chatbot", back_populates="knowledge_base")

    active_status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())