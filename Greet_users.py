from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from app.models.chatbot import Chatbot
from app.models.knowdegde_base import KnowledgeBase
from app.models.user import User
from app.models.session import Session
from app.models.user_chatbot import UserChatbot
from sqlalchemy.orm import joinedload
from app.db import engine, SessionLocal, Base, get_db
from utils.helper import model

db=SessionLocal()

# def get_chatbots_for_user(user_id): #83
#     chatbots = db.query(Chatbot).\
#         join(UserChatbot, UserChatbot.chatbot_id == Chatbot.id).\
#         filter(UserChatbot.user_id == user_id).all()
#     return chatbots

# # Example usage:
# if __name__ == "__main__":
    
#     user_id = 83  # Replace with the actual user ID
#     chatbots = get_chatbots_for_user(user_id)
#     if chatbots:
#         for chatbot in chatbots:
#             print(f"Chatbot ID: {chatbot.id}, Name: {chatbot.name}")
#     else:
#         print("None found")        


# def get_user_details(user_id): #83
#     user = db.query(User).filter(User.id == user_id).first()
#     return user

# # Example usage:
# if __name__ == "__main__":
#     user_id = 93  # Replace with the actual user ID
#     user = get_user_details(user_id)
#     if user:
#         print(f"User ID: {user.id}")
#         print(f"Name: {user.name}")
#         print(f"Email: {user.email}")
#         print(f"Phone: {user.phone}")
#         print(f"Avatar: {user.avatar}")
#         print(f"Is Verified: {user.is_verified}")
#         print(f"Created At: {user.created_at}")
#         print(f"Updated At: {user.updated_at}")
#     else:
#         print("User not found.")

def count_sessions_for_user(user_id):
    session_count = db.query(func.count(Session.id)).\
        join(Chatbot, Session.chatbot_id == Chatbot.id).\
        join(UserChatbot, UserChatbot.chatbot_id == Chatbot.id).\
        filter(UserChatbot.user_id == user_id).scalar()
    return session_count

# Example usage:
if __name__ == "__main__":
    user_id = 83  # Replace with the actual user ID
    session_count = count_sessions_for_user(user_id)
    print(f"User {user_id} has {session_count} sessions.")
