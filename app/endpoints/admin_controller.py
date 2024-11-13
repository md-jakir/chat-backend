from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.models.admin import Admin
from app.schema.admin import AdminBase, AdminCreate, AdminResponse, UpdateAdmin, UpdateAdminPassword, AllAdminResponse
from app.helpers.helper import custom_response_handler

from app.services.admin_service import find_admins, get_admin_by_id, get_admin_by_email, upd_admin_password, save_admin, del_admin, upd_admin, upd_admin_avater

from app.db import get_db

from utils.logger import logger

router = APIRouter()

@router.get("/", response_model=AllAdminResponse)
async def get_admins(skip: int = 0, limit: int = 100, search:str="", db: Session = Depends(get_db)):
    try:
        query = db.query(Admin)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Admin.name.ilike(search_pattern),
                    Admin.email.ilike(search_pattern),
                    Admin.phone.ilike(search_pattern),    
                )
            )

        total = query.count()
        admins = query.order_by(Admin.created_at.desc()).offset(skip*limit).limit(limit).all()

        return {"total": total, "data": admins, "message": "Admins retrieved successfully"}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/{admin_id}", response_model=AdminResponse)
async def get_admin(admin_id: int):
    try:
        admin = await get_admin_by_id(admin_id)
        return custom_response_handler(200, "Admin retrieved successfully", admin)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/email/{email}", response_model=AdminResponse)
async def get_admin_by_email(email: str):
    try:
        admin = await get_admin_by_email(email)
        return custom_response_handler(200, "Admin retrieved successfully", admin)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.post("/", response_model=AdminResponse)
async def create_admin(name: str = Form(...), email: str = Form(...), phone: Optional[str] = Form(None), password:str = Form(...), avatar: UploadFile = File(None)):
    try:
        admin = AdminCreate(name=name, email=email, phone=phone, password=password)
        print(admin)
        created_admin = await save_admin(admin, avatar)
        return custom_response_handler(201, "Admin created successfully", created_admin)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
@router.put("/{admin_id}", response_model=AdminResponse)
async def update_admin(admin: UpdateAdmin, admin_id: int):
    try:
        admin = await upd_admin(admin_id, admin)
        return custom_response_handler(200, "Admin updated successfully", admin)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
@router.put("/{admin_id}/upload-avater", response_model=AdminResponse)
async def upload_avatar(admin_id: int, avatar: UploadFile = File(...)):
    try:
        admin = await upd_admin_avater(admin_id, avatar)
        return custom_response_handler(200, "Avatar uploaded successfully", admin)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e

@router.put("/{admin_id}/update-password", response_model=AdminResponse)
async def update_password(admin_id: int, passwords: UpdateAdminPassword):
    try:
        admin = await upd_admin_password(admin_id, passwords)
        return custom_response_handler(200, "Password updated successfully", admin)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e

@router.delete("/{admin_id}")
async def delete_admin(admin_id: int):
    try:
        await del_admin(admin_id)
        return custom_response_handler(200, "Admin deleted successfully")
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    