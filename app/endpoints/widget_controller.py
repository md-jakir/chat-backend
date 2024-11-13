from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
from sqlalchemy import or_

from app.models.widget_config import WidgetConfig
from app.helpers.helper import custom_response_handler
from app.schema.widget_config_schema import WidgetConfigCreate

from app.db import get_db
from utils.logger import logger  

router = APIRouter()

@router.post("/")
async def create_widget(widget: WidgetConfigCreate = Body(...), db: Session = Depends(get_db)):
    try:
        new_widget = WidgetConfig(**widget.dict())
        db.add(new_widget)
        db.commit()
        return custom_response_handler(201, "Widget created successfully", new_widget)
    except Exception as e:
        logger.error(f"Failed to create widget: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create widget")
    
@router.get("/")
def get_widgets(skip: int, limit: int, search: str = "", db: Session = Depends(get_db)):
    query = db.query(WidgetConfig)
  
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                WidgetConfig.name.ilike(search_pattern)
            )
        )

    try:
        total = query.count()
        widgets = query.order_by(WidgetConfig.id.desc()).offset(skip*limit).limit(limit).all()
        return {"total": total, "data": widgets}
    except Exception as e:
        print(f"Error: {e}")
        return {"total": 0, "data": []}

@router.get("/options")
async def get_widget_options(db: Session = Depends(get_db)):
    try:
        widgets = db.query(WidgetConfig).all()
        options = [{"label": widget.name, "value": widget.id} for widget in widgets]
        return options
    
    except Exception as e:
        logger.error(f"Failed to retrieve widget options: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve widget options")

@router.get("/{widget_id}")
async def get_widget_by_id(widget_id: int, db: Session = Depends(get_db)):
    try:
        widget = db.query(WidgetConfig).filter(WidgetConfig.id == widget_id).first()
        if not widget:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
        return widget
    except Exception as e:
        logger.error(f"Failed to retrieve widget: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve widget")
    
@router.put("/{widget_id}")
async def update_widget(widget_id: int, widget: WidgetConfigCreate = Body(...), db: Session = Depends(get_db)):
    try:
        widget_to_update = db.query(WidgetConfig).filter(WidgetConfig.id == widget_id).first()
        if not widget_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
        for key, value in widget.dict().items():
            setattr(widget_to_update, key, value)
        db.commit()
        return custom_response_handler(200, "Widget updated successfully", widget_to_update)
    except Exception as e:
        logger.error(f"Failed to update widget: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update widget")
    
@router.delete("/{widget_id}")
async def delete_widget(widget_id: int, db: Session = Depends(get_db)):
    try:
        widget_to_delete = db.query(WidgetConfig).filter(WidgetConfig.id == widget_id).first()
        if not widget_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
        db.delete(widget_to_delete)
        db.commit()
        return custom_response_handler(200, "Widget deleted successfully", widget_to_delete)
    except Exception as e:
        logger.error(f"Failed to delete widget: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete widget")
    