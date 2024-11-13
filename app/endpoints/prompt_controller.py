from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path

from app.db import get_db
from app.services.prompt_service import set_prompt,get_prompt,update_prompt,delete_prompt
from app.schema.prompt_schema import Prompt  
from utils.logger import logger  

router = APIRouter()

@router.post("/", response_model=Prompt, status_code=status.HTTP_201_CREATED)
async def create_prompt(prompt_text: str = Form(...), chatbot_id: int = Form(...), db: Session = Depends(get_db)):
    try:
        prompt = set_prompt(db, prompt_text=prompt_text, chatbot_id=chatbot_id)
        return prompt
    except Exception as e:
        logger.error(f"Failed to create prompt: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create prompt")

@router.get("/{prompt_id}", response_model=Prompt)
async def read_prompt(prompt_id: int, db: Session = Depends(get_db)):
    try:
        prompt = get_prompt(db, prompt_id=prompt_id)
        if not prompt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
        return prompt
    except Exception as e:
        logger.error(f"Failed to retrieve prompt: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve prompt")

@router.put("/{prompt_id}", response_model=Prompt)
async def update_prompt_data(prompt_id: int, prompt_text: str = Form(...), db: Session = Depends(get_db)):
    try:
        prompt = update_prompt(db, prompt_id=prompt_id, prompt_text=prompt_text)
        if not prompt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
        return prompt
    except Exception as e:
        logger.error(f"Failed to update prompt: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update prompt")

@router.delete("/{prompt_id}", response_model=Prompt)
async def delete_prompt_data(prompt_id: int, db: Session = Depends(get_db)):
    try:
        prompt = delete_prompt(db, prompt_id=prompt_id)
        if not prompt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
        return prompt
    except Exception as e:
        logger.error(f"Failed to delete prompt: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete prompt")
