from sqlalchemy.orm import Session as DbSession
from fastapi import HTTPException
from utils.logger import logger
from ..models.session import Session
from sqlalchemy.exc import NoResultFound
from typing import Optional

class SessionRepository:
    
    @staticmethod
    def create_or_update_session(db_session: DbSession, token: str, chatbot_id: int, name: str, user_id: Optional[int] = None) -> int:
        try:
            # Check if a session with the given token exists
            existing_session = db_session.query(Session).filter_by(token = token).one_or_none()
            
            if existing_session:
                # If the session with the token exists, return its ID
                return existing_session.id
            else:
                # If the session with the token does not exist, create a new session
                new_session = Session(name = name, token = token, chatbot_id = chatbot_id, user_id = user_id)
                db_session.add(new_session)
                db_session.commit()
                # Return the ID of the newly created session
                return new_session.id

        except Exception as e:
            db_session.rollback()
            raise e