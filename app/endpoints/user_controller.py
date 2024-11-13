from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import aliased


from app.db import get_db
from app.models.user import User
from app.models.user_chatbot import UserChatbot
from app.schema.user import UserBase, UserResponse, UpdateUserPassword, UserResponseWithMessage, UpdateUser
from utils.logger import logger
from app.services.user import find_users, upd_user_avater, save_user, del_user, upd_user, upd_user_password, chatbot_by_user,get_user_by_id
from app.helpers.helper import custom_response_handler
from sqlalchemy import or_

router = APIRouter()


@router.get("/", response_model=UserResponseWithMessage)
async def get_users(skip: int = 0, limit: int = 10, search:str="", db: Session = Depends(get_db)):
    try:
        query = db.query(User)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    User.name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    User.phone.ilike(search_pattern),
                    
                )
            )

        total = query.count()
        users = query.order_by(User.created_at.desc()).offset(skip*limit).limit(limit).all()

        return {"total": total, "data": users, "message": "Users retrieved successfully"}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
#user as options
# value should be options = [
#   { value: id, label: 'Chris' },
#   { value: id, label: 'John' },
#   { value: id, label: 'Jane' },
#   { value: id, label: 'Kate' },
#   { value: id, label: 'Sarah' },
#   { value: id, label: 'Mike' },
# ]
@router.get("/all/options")
async def get_users_options(chatbotId: str= '',db: Session = Depends(get_db)):
    try:
        if(chatbotId == ''):
            UserAlias = aliased(User) 
            users = db.query(UserAlias.id, UserAlias.email).all()
            
            options = [{"value": user_id, "label": email} for user_id, email in users]
            
            return options        
        else:
            UserAlias = aliased(User) 
            userChatbot = db.query(UserChatbot).filter(UserChatbot.chatbot_id == chatbotId).all()

            userChatbotList = []

            for user in userChatbot:
                userChatbotList.append(user.user_id)
            
            users = db.query(UserAlias.id, UserAlias.email).filter(UserAlias.id.not_in(userChatbotList)).all()
            
            options = [{"value": user_id, "label": email} for user_id, email in users]
            
            return options
        # for userChatbot in userChatbotList:
        #     print(userChatbot)
        UserAlias = aliased(User) 
        users = db.query(UserAlias.id, UserAlias.email).all()
        
        options = [{"value": user_id, "label": email} for user_id, email in users]
        
        return userChatbotList
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    try:
        user = await get_user_by_id(user_id)
        return custom_response_handler(200, "User retrieved successfully", user)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.get("/{user_id}/chatbot")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        chatbot = chatbot_by_user(db, user_id)
        return chatbot
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/", response_model=UserResponse)
async def create_user(user: UserBase):
    try:
        created_user = await save_user(user)
        return custom_response_handler(201, "User created successfully", created_user)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user: UpdateUser, user_id: int):
    try:
        user = await upd_user(user_id, user)
        return custom_response_handler(200, "User updated successfully", user)
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e

@router.put("/{user_id}/upload-avater", response_model=UserResponse)
async def upload_avatar(user_id: int, avatar: UploadFile = File(...)):
    user = await upd_user_avater(user_id, avatar)
    return custom_response_handler(200, "Avatar uploaded successfully", user)

@router.put("/{user_id}/update-password", response_model=UserResponse)
async def update_password(user_id: int, passwords: UpdateUserPassword):
    user = await upd_user_password(user_id, passwords)

    return custom_response_handler(200, "Password updated successfully", user)


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    try:
        await del_user(user_id)
        return custom_response_handler(200, "User deleted successfully")
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e