from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.db import Base
from sqlalchemy.orm import relationship

class SampleQustion(Base):
    __tablename__ = 'sample_qustion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
   
    chatbot_id = Column(Integer, ForeignKey('chatbot.id'), default=None)
    chatbot = relationship("Chatbot", back_populates="sample_qustion")
    