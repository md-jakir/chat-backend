from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func,Boolean
from app.db import Base
from sqlalchemy.orm import relationship

class SessionHistory(Base):
    __tablename__ = 'session_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    qustion = Column(String(65535))
    answer = Column(String(65535))
    feedback = Column(Boolean, default=None, nullable=True)
    text_feedback = Column(String(65535))
    response_time = Column(String(255))
    cost = Column(String(255))
    session_id = Column(Integer, ForeignKey('session.id'), default=None)
    session = relationship("Session", back_populates="session_history")
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
