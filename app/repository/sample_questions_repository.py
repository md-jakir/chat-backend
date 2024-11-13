from sqlalchemy.orm import Session as SQLASession
from fastapi import HTTPException
from utils.logger import logger
from ..models.session import Session
from ..models.session_hiostory import SessionHistory
from ..models.sample_qustion import SampleQustion
from sqlalchemy.exc import NoResultFound
from langchain_core.messages import AIMessage, HumanMessage
from sqlalchemy import desc

class SampleQuestionsRepository:
    @staticmethod
    def get_history(db_session: SQLASession, chatbot_id: int) -> list:
        try:
            questions = db_session.query(SampleQustion.text).filter_by(chatbot_id=chatbot_id).all()
            if not questions:
                return []
            questions = [q.text for q in questions]
            print(questions)
            return questions
        except Exception as e:
                logger.error(f"An error occurred while fetching sample questions: {e}")
                raise e
        
