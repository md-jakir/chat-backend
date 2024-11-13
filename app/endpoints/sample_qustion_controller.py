import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.models.sample_qustion import SampleQustion

from app.schema.sample_qustion import SampleQuestionBase, SampleQuestionResponse

from app.db import get_db
from utils.logger import logger

router = APIRouter()

@router.get("/")
def get_sample_qustions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        total = db.query(SampleQustion).count()
        sample_qustions = db.query(SampleQustion).offset(skip).limit(limit).all()

        return {"total": total, "data": sample_qustions}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/by_chatbot/{chatbot_id}")
def get_sample_qustions_by_chatbot(chatbot_id: int, db: Session = Depends(get_db)):
    try:
        sample_qustions = db.query(SampleQustion).filter(SampleQustion.chatbot_id == chatbot_id).all()
        if not sample_qustions:
            raise HTTPException(status_code=404, detail="Sample questions not found for the given chatbot ID")

        return {"data": sample_qustions}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    
@router.get("/{sample_qustion_id}")
def get_sample_qustion(sample_qustion_id: int, db: Session = Depends(get_db)):
    try:
        sample_qustion = db.query(SampleQustion).filter(SampleQustion.id == sample_qustion_id).first()
        if not sample_qustion:
            raise HTTPException(status_code=404, detail="SampleQustion not found")
        return sample_qustion
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.post("/")
async def create_sample_qustion(sample_question: SampleQuestionBase, db: Session = Depends(get_db)):
    try:
        sample_qustion = SampleQustion(text=sample_question.text, chatbot_id=sample_question.chatbot_id )
        db.add(sample_qustion)
        db.commit()
        db.refresh(sample_qustion)
        return {
            "message": "Qustion created successfully",  
        }
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/{sample_qustion_id}")
async def update_sample_qustion(sample_qustion_id: int, sample_question: SampleQuestionBase, db: Session = Depends(get_db)):
    try:
        sample_qustion = db.query(SampleQustion).filter(SampleQustion.id == sample_qustion_id).first()
        if not sample_qustion:
            raise HTTPException(status_code=404, detail="SampleQustion not found")
        sample_qustion.text = sample_question.text
        sample_qustion.chatbot_id = sample_question.chatbot_id
        db.commit()
        db.refresh(sample_qustion)
        return {
            "message": "Qustion updated successfully",
        }
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.delete("/{sample_qustion_id}")
async def delete_sample_qustion(sample_qustion_id: int, db: Session = Depends(get_db)):
    try:
        sample_qustion = db.query(SampleQustion).filter(SampleQustion.id == sample_qustion_id).first()
        if not sample_qustion:
            raise HTTPException(status_code=404, detail="SampleQustion not found")
        db.delete(sample_qustion)
        db.commit()
        return {
            "message": "Qustion deleted successfully",  
        }
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")