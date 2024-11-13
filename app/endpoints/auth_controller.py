from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db

from app.models.user import User
from app.models.admin import Admin
from app.models.otp import OTP

from app.services.user import get_user_by_email

from utils.logger import logger
# from app.services.user import find_users, save_user, del_user, upd_user
from app.helpers.hash_password import check_password
from app.helpers.auth import create_access_token, token_for_verification, verify_token
from app.schema.auth import AuthLoginBase, AuthLoginResponse, AuthAdminResponse, AuthRegisterBase, RegisterUserResponse
from app.schema.auth import GoogleLoginDTO, GoogleUserDTO, GoogleAuthUser, TokenResponse
from app.helpers.helper import custom_response_handler, send_email, generate_otp
import os
import requests

router = APIRouter()


@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email.ilike(email)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        otp = generate_otp()

        isExist = db.query(OTP).filter(OTP.user_id == user.id, OTP.user_role == "user").first()

        if(isExist):
            isExist.otp = otp
            db.commit()
            db.refresh(isExist)
        else:
            otp = OTP(otp=otp, user_id=str(user.id), user_role="user")
            db.add(otp)
            db.commit()
            db.refresh(otp)

        html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Forgot Password OTP</title>
            </head>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                <div style="background-color: #ffffff; max-width: 600px; margin: 50px auto; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <div style="text-align: center; padding: 10px 0;">
                        <img src="logo-url-here" alt="Company Logo" style="width: 100px;">
                    </div>
                    <div style="padding: 20px;">
                        <h2>Forgot Password Request</h2>
                        <p>Dear [User's Name],</p>
                        <p>We received a request to reset your password. Use the OTP below to reset your password:</p>
                        <div style="font-size: 24px; font-weight: bold; text-align: center; margin: 20px 0;">[OTP_CODE]</div>
                        <p>This OTP is valid for 30 minutes. If you did not request a password reset, please ignore this email or contact support.</p>
                        <p>Best regards,<br>Your Company Name</p>
                    </div>
                    <div style="text-align: center; padding: 10px; color: #888888; font-size: 12px;">
                        <p>&copy; 2024 Your Company Name. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
        
        user_name = user.name
        if(isExist):
            opt_code = isExist.otp
        else:
            opt_code = otp.otp
        company_name = "Brain Station 23"
        company_logo_url = "https://brainstation-23.com/wp-content/uploads/2024/02/Logo_BS23_Rectangle_Cyan.svg"

        html = html.replace("[User's Name]", user_name)
        html = html.replace("[OTP_CODE]", opt_code)
        html = html.replace("Your Company Name", company_name)
        html = html.replace("logo-url-here", company_logo_url)


        subject = "Your OTP Code for Password Reset"
        send_email(email, subject, html)   
        return {"status_code": 200, "message": "Email sent successfully"}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e

@router.post("/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email.ilike(email)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        otp_obj = db.query(OTP).filter(OTP.user_id == user.id, OTP.user_role == "user").first()
        if not otp_obj:
            raise HTTPException(status_code=404, detail="OTP not found")
        if otp_obj.otp != otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        db.delete(otp_obj)
        db.commit()
        
        user.is_verified = True
        db.commit()
        db.refresh(user)

        return {"status_code": 200, "message": "OTP verified successfully"}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
@router.post("/reset-password")
def reset_password(email: str, password: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email.ilike(email)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if(user.is_verified == False or user.is_verified == None):
            raise HTTPException(status_code=400, detail="User not verified. Please verify your email first.")
        user.password = User.hash_password(password)
        db.commit()
        db.refresh(user)
        return {"status_code": 200, "message": "Password reset successfully"}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e


@router.post("/login", response_model=AuthLoginResponse)
async def login(login_data: AuthLoginBase, db: Session = Depends(get_db)):
    try:
        
        user = db.query(User).filter(User.email.ilike(login_data.email)).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        isPassCorrect = check_password(login_data.password, user.password)
        if not isPassCorrect:
            raise HTTPException(status_code=400, detail="Incorrect password")
    
        access_token = create_access_token(data={"sub": user.email})
       
        return {"status_code": 200, "message": "Login successful", "user": user, "access_token": access_token, "token_type": "bearer"}

    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
@router.post("/register", response_model=RegisterUserResponse)
def register(user: AuthRegisterBase, db: Session = Depends(get_db)):
    try:
        user_dict = user.model_dump()
        user_dict["password"] = User.hash_password(user_dict["password"])
        user = User(**user_dict)
        db.add(user)
        db.commit()
        db.refresh(user)
        return custom_response_handler(201, "User created successfully", user)
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/google/authorize")
def google_authorize(googleLoginDto: GoogleLoginDTO, db: Session = Depends(get_db)):
    try:
        google_response = requests.get(f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={googleLoginDto.token}")
        if google_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid token")
        authorized_user = GoogleUserDTO(**google_response.json())
        # create a new object with name and email
       
        user = db.query(User).filter(User.email.ilike(authorized_user.email)).first()

        if not user:
            user_dict = {"name": authorized_user.name, "email": authorized_user.email}
            user = User(**user_dict)
            db.add(user)
            db.commit()
            db.refresh(user)
        
        access_token = create_access_token(data={"email": user.email, "name": user.name, "role": "admin", "sub": user.email, "role": "user", "id": user.id})

        response = {
            "status_code": 200,
            "message": "Login successful",
            "user": user,
            "token": access_token,
        }

        return response
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
       


@router.post("/admin/login", response_model=AuthAdminResponse)
async def admin_login(login_data: AuthLoginBase, db: Session = Depends(get_db)):
    try:
        admin = db.query(Admin).filter(Admin.email.ilike(login_data.email)).first()

        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        isPassCorrect = check_password(login_data.password, admin.password)
        if not isPassCorrect:
            raise HTTPException(status_code=400, detail="Incorrect password")
    
        access_token = create_access_token(data={"email": admin.email, "name": admin.name, "role": "admin", "sub": admin.email, "role": "admin", "id": admin.id, "phone": admin.phone, "avatar": admin.avatar})
       
        return {"status_code": 200, "message": "Login successful", "admin": admin, "access_token": access_token, "token_type": "bearer"}

    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
@router.post("/admin/register", response_model=RegisterUserResponse)
def admin_register(admin: AuthRegisterBase, db: Session = Depends(get_db)):
    try:
        admin_dict = admin.model_dump()
        admin_dict["password"] = Admin.hash_password(admin_dict["password"])
        admin = Admin(**admin_dict)
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return custom_response_handler(201, "Admin created successfully", admin)
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
@router.post("/admin/forgot-password")
def admin_forgot_password(email: str, db: Session = Depends(get_db)):
    try:
        admin = db.query(Admin).filter(Admin.email == email).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        token = token_for_verification({"email": admin.email})

        html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Forgot Password Token</title>
            </head>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                <div style="background-color: #ffffff; max-width: 600px; margin: 50px auto; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <div style="text-align: center; padding: 10px 0;">
                        <img src="logo-url-here" alt="Company Logo" style="width: 100px;">
                    </div>
                    <div style="padding: 20px;">
                        <h2>Forgot Password Request</h2>
                        <p>Dear [Admin's Name],</p>
                        <p>We received a request to reset your password. Use the token below to reset your password:</p>
                        <div style="font-size: 24px; font-weight: bold; text-align: center; margin: 20px 0;">
                        <a href="BASE_URL/reset-password?token=[TOKEN]">Click
                        here</a></div>
                        </div>
                        <p>This token is valid for 30 minutes. If you did not request a password reset, please ignore this email or contact support.</p>
                        <p>Best regards,<br>Your Company Name</p>
                    </div>
                    <div style="text-align: center; padding: 10px; color: #888888; font-size: 12px;">
                        <p>&copy; 2024 Your Company Name. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
        BASE_URL = os.getenv("BASE_URL")
        admin_name = admin.name
        token = token
        company_name = "Brain Station 23"
        company_logo_url = "https://brainstation-23.com/wp-content/uploads/2024/02/Logo_BS23_Rectangle_Cyan.svg"

        html = html.replace("[Admin's Name]", admin_name)
        html = html.replace("[TOKEN]", token)
        html = html.replace("Your Company Name", company_name)
        html = html.replace("logo-url-here", company_logo_url)
        html = html.replace("BASE_URL", BASE_URL)

        subject = "Your OTP Code for Password Reset"
        send_email(email, subject, html)   
        return {"status_code": 200, "message": "Email sent successfully"}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    
@router.post("/admin/reset-password")
def admin_reset_password(token: str, password: str, db: Session = Depends(get_db)):
    try:
        payload = verify_token(token)
        email = payload.get("email")
        admin = db.query(Admin).filter(Admin.email == email).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        admin.password = Admin.hash_password(password)
        db.commit()
        db.refresh(admin)
        return {"status_code": 200, "message": "Password reset successfully"}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e 

