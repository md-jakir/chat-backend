from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from app.db import Base
from passlib.hash import bcrypt

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True, default=None)
    avatar = Column(String(255), nullable=True, default=None)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    @staticmethod
    def hash_password(password):
        return bcrypt.hash(password)
    
    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.verify(password, hashed_password)