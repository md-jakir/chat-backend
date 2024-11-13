from sqlalchemy import Column, String, DateTime, Enum, Integer, func
from app.db import Base
from datetime import datetime, timedelta
from enum import Enum as PythonEnum


class UserType(PythonEnum):
    user = "user"
    admin = "admin"

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    otp = Column(String, index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    user_role = Column(Enum(UserType), default=UserType.user, index=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, default=func.now() + timedelta(minutes=30))
