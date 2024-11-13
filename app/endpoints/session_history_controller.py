from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session 
from typing import List
from pathlib import Path
from app.db import get_db
from sqlalchemy import or_

from sqlalchemy.orm import joinedload

from app.models.session_hiostory import SessionHistory
from utils.logger import logger


router = APIRouter()

@router.get("/")
def get_session_history(skip: int = 0, limit: int = 100, search: str = "", db: Session = Depends(get_db)):
    try:
        query = db.query(SessionHistory)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    SessionHistory.qustion.ilike(search_pattern),
                    SessionHistory.answer.ilike(search_pattern),
                    SessionHistory.text_feedback.ilike(search_pattern),
                    SessionHistory.response_time.ilike(search_pattern),
                    SessionHistory.cost.ilike(search_pattern)
                )
            )

        total = query.count()
        session_history = query.order_by(SessionHistory.created_at.desc()).offset(skip * limit).limit(limit).all()

        return {"total": total, "data": session_history}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/{session_history_id}")
def get_session_history(session_history_id: int, db: Session = Depends(get_db)):
    try:
        session_history = db.query(SessionHistory).filter(SessionHistory.id == session_history_id).first()
        if not session_history:
            raise HTTPException(status_code=404, detail="SessionHistory not found")
        return session_history
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
# @router.post("/")
# async def create_session_history(session_history: SessionHistory, db: Session = Depends(get_db)):
#     try:
#         db.add(session_history)
#         db.commit()
#         db.refresh(session_history)
#         return session_history
#     except HTTPException as e:
#         logger.info(f'An HTTP error occurred: \n {str(e)}')
#         raise e
#     except Exception as e:
#         logger.info(f'An error occurred: \n {str(e)}')
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
# @router.put("/{session_history_id}")
# async def update_session_history(session_history_id: int, session_history: SessionHistory, db: Session = Depends(get_db)):
#     try:
#         db.query(SessionHistory).filter(SessionHistory.id == session_history_id).update(session_history)
#         db.commit()
#         return {"message": "SessionHistory updated successfully"}
#     except HTTPException as e:
#         logger.info(f'An HTTP error occurred: \n {str(e)}')
#         raise e
#     except Exception as e:
#         logger.info(f'An error occurred: \n {str(e)}')
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.delete("/{session_history_id}")
async def delete_session_history(session_history_id: int, db: Session = Depends(get_db)):
    try:
        db.query(SessionHistory).filter(SessionHistory.id == session_history_id).delete()
        db.commit()
        return {"message": "SessionHistory deleted successfully"}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    
