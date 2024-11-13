from sqlalchemy.orm import Session as SQLASession
from fastapi import HTTPException
from utils.logger import logger
from ..models.session import Session
from ..models.session_hiostory import SessionHistory
from sqlalchemy.exc import NoResultFound
from langchain_core.messages import AIMessage, HumanMessage
from sqlalchemy import desc

class SessionHistoryRepository:
    
    @staticmethod
    def set_history(db_session: SQLASession, session_id: int, question: str, answer: str,cost: str,response_time: str) -> SessionHistory:
        try:
            # Create a new session history entry
            new_history = SessionHistory(
                qustion=question,
                answer=answer,
                text_feedback="",
                response_time=response_time,
                cost=cost,
                session_id=session_id
            )
            db_session.add(new_history)
            db_session.commit()
            return new_history

        except Exception as e:
            db_session.rollback()
            raise e

    @staticmethod
    def get_history(db_session: SQLASession, session_id: int) -> list:
            try:
                # Retrieve all session history entries for the given session_id, ordered by created_at in descending order
                # history = (db_session.query(SessionHistory)
                #         .filter_by(session_id=session_id)
                #         .all())
                
                history = (db_session.query(SessionHistory)
                        .filter_by(session_id=session_id)
                        .order_by(SessionHistory.created_at.desc())
                        .limit(2)
                        .all())
                                
                # Check if the history is empty
                if not history:
                    return []

                # Process the results into a list of HumanMessage and AIMessage objects
                chat_history = []
                for entry in history:
                    chat_history.append(AIMessage(content=entry.answer))
                    chat_history.append(HumanMessage(content=entry.qustion))
                
                chat_history.reverse()
                
                logger.info(f"chat_history: \n {chat_history}")
                return chat_history

            except Exception as e:
                logger.error(f"An error occurred while fetching chat history: {e}")
                raise e
            
    @staticmethod
    def get_history_json(chats: SessionHistory) -> dict:
        return {i:{"question": chat.qustion, "answer": chat.answer} for i,chat in enumerate(chats)}