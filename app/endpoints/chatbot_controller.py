from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path

from sqlalchemy.orm import joinedload, aliased
from sqlalchemy import select, or_
import os

from app.models.chatbot import Chatbot
from app.models.knowdegde_base import KnowledgeBase
from app.models.sample_qustion import SampleQustion
from app.models.prompt import Prompt
from app.models.user import User
from app.schema.chatbot import PromptBase, UpdateChatbotBase, QueryInput, FeedBack,AWSQueryInput

from app.models.user_chatbot import UserChatbot

from app.db import get_db
from utils import set_user_feedback
from utils.logger import logger
from utils.pdf_qna import upload_pdf_chain_call
from utils.pdf_utils import process_uploaded_pdfs
from utils.sample_q import  get_sample_questions
from utils.pdf_qna_multiturn import run_multiturn_doc_chain
# from utils.helper import bedrock,model as M
from app.repository.session_repository import SessionRepository
from langchain_aws import ChatBedrock
from utils.classify_routes import classify_routes
from utils.helper import text_streamer, bedrock
from utils.helper import model as openaimodel
from utils.greetings import greet_chain
from app.helpers.custom_exception_handler import chat_error_message
from langdetect import detect


# sessions = {}

router = APIRouter()

@router.get("/")
async def get_chatbots(skip: int = 0, limit: int = 10, search: str = "", db: Session = Depends(get_db)):
    try:
        query = db.query(Chatbot)
        if(search):
            search_parttern = f"%{search}%"
            query = query.filter(
                or_(
                    Chatbot.name.ilike(search_parttern),
                    Chatbot.gretting_message.ilike(search_parttern)
                )
            )
        total = query.count()
        chatbots = query.options(joinedload(Chatbot.user_chatbot), joinedload(Chatbot.knowledge_base), joinedload(Chatbot.sample_qustion), joinedload(Chatbot.session)).order_by(Chatbot.created_at.desc()).offset(skip * limit).limit(limit).all()
        return {"total": total, "data": chatbots}    
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/{chatbot_id}")
def get_chatbot(chatbot_id: int, db: Session = Depends(get_db)):
    try:
        SampleQuestionAlias = aliased(SampleQustion)
        subquery = (
            select(SampleQuestionAlias.id)
            .where(SampleQuestionAlias.chatbot_id == chatbot_id)
            .order_by(SampleQuestionAlias.id) 
            .limit(6)
            .subquery()
)
        chatbot = (
            db.query(Chatbot)
            .options(
                joinedload(Chatbot.knowledge_base),
                joinedload(Chatbot.sample_qustion.and_(SampleQustion.id.in_(subquery))),
                joinedload(Chatbot.session)
            )
            .filter(Chatbot.id == chatbot_id)
            .first()
        )
        
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        return chatbot
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/{chatbot_id}/knowledge_base")
def get_knowledge_base(chatbot_id: int, db: Session = Depends(get_db)):
    try:
        knowledge_base = db.query(KnowledgeBase).filter(KnowledgeBase.chatbot_id == chatbot_id).all()   
        return knowledge_base
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{chatbot_id}/prompt")
def get_prompt(chatbot_id: int, db: Session = Depends(get_db)):
    try:
        prompt = db.query(Prompt).filter(Prompt.chatbot_id == chatbot_id).first()   
        return prompt
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/{chatbot_id}/sample_qustion")
def get_sample_qustion(chatbot_id: int, db: Session = Depends(get_db)):
    try:
        sample_qustion = db.query(SampleQustion).order_by(SampleQustion.created_at.desc()).filter(SampleQustion.chatbot_id == chatbot_id).limit(6).all() 
        return sample_qustion
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{chatbot_id}/assigned_users")
def get_assigned_users(chatbot_id: int, skip: int = 0, limit: int = 10, search: str = "", db: Session = Depends(get_db)):
    try:
        query = db.query(UserChatbot)
        if(search):
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    UserChatbot.user.has(User.name.ilike(search_pattern)),
                    UserChatbot.user.has(User.email.ilike(search_pattern)),
                    UserChatbot.user.has(User.phone.ilike(search_pattern))
                )
            )
        total = query.count()
        assigned_users = query.options(joinedload(UserChatbot.user)).filter(UserChatbot.chatbot_id == chatbot_id).order_by(UserChatbot.created_at.desc()).offset(skip * limit).limit(limit).all()

        return {"total": total, "data": assigned_users}  
        
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/knowledge_base/all")
def get_knowledge_base(db: Session = Depends(get_db)):
    try:
        knowledge_base = db.query(KnowledgeBase).all()
        return knowledge_base
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.post("/")
async def create_chatbot(name: str = Form(...), gretting_message: str = Form(...) ,files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
        new_chatbot = Chatbot(name=name, gretting_message=gretting_message)
        db.add(new_chatbot)
        db.commit()
        db.refresh(new_chatbot)

        if(new_chatbot):
            files_location = await process_uploaded_pdfs(files, new_chatbot.id)

            new_knowledge_base = [KnowledgeBase(path=file["path"], chatbot_id=file["chatbot_id"]) for file in files_location["files"]] 
            db.add_all(new_knowledge_base)
            db.commit()
            for instance in new_knowledge_base:
                db.refresh(instance)
            new_chatbot.knowledge_base_path = files_location["root_path"]
            
            questions=get_sample_questions(new_chatbot.id) 
            
            print(f"sample_questions: {len(questions)}")
            
            
            db.commit()
            # Create a list of SampleQustion instances
            sample_questions = [SampleQustion(text=question_text, chatbot_id=new_chatbot.id) for question_text in questions]
            
            db.add_all(sample_questions)
            db.commit()
               
        
        return {
            "message": "Chatbot created successfully",
            "chatbot": {
                "id": new_chatbot.id,
                "name": new_chatbot.name,
                "gretting_message": new_chatbot.gretting_message,
                "knowledge_base": {
                    "id": new_knowledge_base[0].id if new_knowledge_base else None,
                    "files": [file.path for file in new_knowledge_base],
                    "updated_at": new_knowledge_base[0].updated_at if new_knowledge_base else None ,
                    "created_at": new_knowledge_base[0].created_at if new_knowledge_base else None 

                }
            },
        }
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e

@router.put("/{chatbot_id}")
def update_chatbot(chatbot_id: int, chatbot: UpdateChatbotBase, db: Session = Depends(get_db)):
    try:
        chatbot_db = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
        if not chatbot_db:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        if(chatbot.name):
            chatbot_db.name = chatbot.name
        if(chatbot.gretting_message):
            chatbot_db.gretting_message = chatbot.gretting_message
        if(chatbot.active_status):
            chatbot_db.active_status = chatbot.active_status
        db.commit()
        db.refresh(chatbot_db)
        return {
            "message": "Chatbot updated successfully",
            "data": {
                "id": chatbot_db.id,
                "name": chatbot_db.name,
                "gretting_message": chatbot_db.gretting_message,
                "active_status": chatbot_db.active_status
            },
        }
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/{chatbot_id}/active_status")
def update_active_status(chatbot_id: int, active_status: bool, db: Session = Depends(get_db)):
    try:
        chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        chatbot.active_status = active_status
        db.commit()
        db.refresh(chatbot)
        return {
            "message": "Active status updated successfully",
            "data": {
                "id": chatbot.id,
                "name": chatbot.name,
                "gretting_message": chatbot.gretting_message,
                "active_status": chatbot.active_status
            },
        }
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/{chatbot_id}/knowledge_base")
async def update_knowledge_base(chatbot_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
      
        chatbot = db.query(Chatbot).options(joinedload(Chatbot.knowledge_base)).filter(Chatbot.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        

        if(chatbot):
            files_location = await process_uploaded_pdfs(files, chatbot.id)

            new_knowledge_base = [KnowledgeBase(path=file["path"], chatbot_id=file["chatbot_id"]) for file in files_location["files"]] 
            db.add_all(new_knowledge_base)
            db.commit()
            for instance in new_knowledge_base:
                db.refresh(instance)
            chatbot.knowledge_base_path = files_location["root_path"]
            
            # questions=get_sample_questions(chatbot.id) 
            # db.commit()
            # # Create a list of SampleQustion instances
            # sample_questions = [SampleQustion(text=question_text, chatbot_id=chatbot.id) for question_text in questions]
            # db.add_all(sample_questions)
            # db.commit()

        return {
            "message": "Knowledge base updated successfully",
            # "knowledge_base": {
            #     "id": new_knowledge_base[0].id if new_knowledge_base else None,
            #     "files": [file.path for file in new_knowledge_base],
            #     "updated_at": new_knowledge_base[0].updated_at if new_knowledge_base else None ,
            #     "created_at": new_knowledge_base[0].created_at if new_knowledge_base else None 
            # },
        }
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/{chatbot_id}/prompt")
def update_prompt(chatbot_id: int, body: PromptBase, db: Session = Depends(get_db)):
    try:
        promptByChatbotId = db.query(Prompt).filter(Prompt.chatbot_id == chatbot_id).first()    
        if not promptByChatbotId:
            newPrompt = Prompt(prompt_text=body.prompt, chatbot_id=chatbot_id)
            db.add(newPrompt)
            db.commit()
            db.refresh(newPrompt)
        else:
            promptByChatbotId.prompt_text = body.prompt
            db.commit()
            db.refresh(promptByChatbotId)


        return {
            "message": "Prompt updated successfully",
        }
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.delete("/{chatbot_id}")
def delete_chatbot(chatbot_id: int, db: Session = Depends(get_db)):
    try:
        chatbot = db.query(Chatbot).options(joinedload(Chatbot.knowledge_base)).filter(Chatbot.id == chatbot_id).first()
      
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        db.delete(chatbot)
        db.commit()
        return {"message": "Chatbot deleted successfully"}
    except HTTPException as e:
        logger.info(f'An HTTP error occurred: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occurred: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
# @router.delete("/knowledge_base/all")
# def delete_knowledge_base(db: Session = Depends(get_db)):
#     try:
#         db.query(KnowledgeBase).delete()
#         db.query(Chatbot).delete()
#         db.commit()
#         return {"message": "Knowledge base deleted successfully"}
#     except HTTPException as e:
#         logger.info(f'An HTTP error occurred: \n {str(e)}')
#         raise e
#     except Exception as e:
#         logger.info(f'An error occurred: \n {str(e)}')
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/chat")  #fixed this function
def pdf_qna(input_data:QueryInput, db: Session = Depends(get_db)):
    question= input_data.question
    chatbot_id = input_data.chatbot_id
    token =input_data.token
    user_id=input_data.user_id
    # model_id = input_data.model_id
    model = db.query(UserChatbot).filter_by(chatbot_id=chatbot_id, user_id=user_id).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    model_id = model.model_id
    if not model_id:
        model_id = "0"

    first_two_words = ' '.join(question.split()[:2])

    ##get session id 
    session_id=SessionRepository.create_or_update_session(db,token,chatbot_id, first_two_words, user_id)
    
    route=classify_routes(question)
    
    if route == "prompt_injection":
        logger.info(f"Prompt injection detected. Ignoring the above directions and doing something else.")
        return StreamingResponse(text_streamer("For security reasons, I can't perform that action. Please ensure your queries are relevant to our conversation topic. Thank you!"), media_type="text/event-stream")
    elif route == "hi":
        logger.info(f"Answering From hi route")
        return StreamingResponse(greet_chain(question), media_type="text/event-stream")
    elif route == "bye":
        logger.info(f"Answering From bye route")
        return StreamingResponse(greet_chain(question), media_type="text/event-stream")
        
    
    print(session_id)
    
    kb_path=Path(f"./data/uploaded_pdf_retriever/{chatbot_id}")
    
    if not session_id:
        session_id= "1234default"
    
    if not question or not session_id:
        logger.info("Invalid input. Please provide a question and session_id")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input. Please provide a question, session_id and user_id")
    
    detected_lang=detect(question)
    try:
        if model_id == "0":
            logger.info(f"Answering From Openai")
            # model_id="mistral.mistral-7b-instruct-v0:2"
            return StreamingResponse(upload_pdf_chain_call(session_id,question,kb_path,db,chatbot_id,openaimodel,detected_lang), media_type="text/event-stream") 
        else:
            if model_id == "1":
                logger.info(f"Answering From mistral-7b-instruct-v0:2")
                model_name="mistral.mistral-7b-instruct-v0:2"
            elif model_id =="2":
                logger.info(f"Answering From amazon.titan-text-express-v1")
                model_name="amazon.titan-text-express-v1"
            elif model_id =="3":
                logger.info(f"Answering From mistral.mistral-large-2402-v1:0")
                model_name="mistral.mistral-large-2402-v1:0"
            elif model_id =="4":
                logger.info(f"Answering From amazon.titan-text-premier-v1:0")
                model_name="amazon.titan-text-premier-v1:0"
            else : 
                logger.info(f"No model found")
                return StreamingResponse(chat_error_message())

            model= ChatBedrock(
                model_id = model_name,
                model_kwargs = dict(temperature=0.025),
                client = bedrock,
            )
            return StreamingResponse(upload_pdf_chain_call(session_id, question,kb_path, db, chatbot_id, model,detected_lang), media_type="text/event-stream")

        # return StreamingResponse(upload_pdf_chain_call(session_id,question,kb_path,db,chatbot_id), media_type="text/event-stream") 
    except HTTPException as e: 
        logger.info(f'An http error occured: \n {str(e)}')
        return StreamingResponse(chat_error_message())
        # raise e
    except Exception as e:
        logger.info(f'An error occured: \n {str(e)}')
        return StreamingResponse(chat_error_message())
        # raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    # # kb= db.query('SELECT id FROM knowledge_base WHERE chatbot_id={chatbotId} and active_status=1')
    # # kb_path= db.query(KnowledgeBase.path).filter(KnowledgeBase.chatbot_id == chatbotId,KnowledgeBase.active_status == 1).all()

    # data= db.query(Chatbot).options(joinedload(Chatbot.user), joinedload(Chatbot.knowledge_base)).filter(Chatbot.id == 1).first()
    # # db.execute('select * from chatbot')
    # print(data)
    # ## kb should be a data storage path

    # print("input data: \n")
    # print(question, "\n", session_id, "\n", chatbotId)
    
    # return data
    # # if not session_id:
    # #     session_id= "1234default"
    
    # # if not question or not session_id:
    # #     logger.info("Invalid input. Please provide a question and session_id")
    # #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input. Please provide a question, session_id and user_id")
    
    # # try:
    # #     return StreamingResponse(upload_pdf_chain_call(sessions,session_id,question,kb_path), media_type="text/event-stream") 
    # # except HTTPException as e: 
    # #     logger.info(f'An http error occured: \n {str(e)}')
    # #     raise e
    # # except Exception as e:
    # #     logger.info(f'An error occured: \n {str(e)}')
    # #     raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/feedback")
def user_feedback(feedback: FeedBack, db: Session = Depends(get_db)):
    if not feedback.user_input:
        feedback.user_input = True
        
    resp = set_user_feedback(feedback.session_id, feedback.query_id, int(feedback.user_feedback), feedback.text_feedback, db)
    return {
        "Response": resp
    }




@router.post("/sample_question_generate") 
def sample_question_test():
    chatbot_id=25 
    questions=get_sample_questions(chatbot_id)
    print(type(questions))
    
    return {
    "message": questions   

    }

#AWS CHAT




# @router.post("/chat_aws")  #fixed this function
# def chat_aws(input_data:AWSQueryInput, db: Session = Depends(get_db)):
#     question= input_data.question
#     chatbot_id = input_data.chatbot_id
#     token =input_data.token
#     model_id=input_data.model_id
    
#     if model_id == "1":
#         logger.info(f"Answering From mistral-7b-instruct-v0:2")
#         model_id="mistral.mistral-7b-instruct-v0:2"
#     elif model_id =="2":
#         logger.info(f"Answering From amazon.titan-text-express-v1")
#         model_id="amazon.titan-text-express-v1"

    
#     model= ChatBedrock(
#         model_id=model_id,
#         model_kwargs=dict(temperature=0),
#         client=bedrock,

#     )
    
#     ##get session id 
#     session_id=SessionRepository.create_or_update_session(db,token,chatbot_id,"session_test1")
    
#     #get chathistory
    
    
#     print(session_id)
    
#     kb_path=Path(f"./data/uploaded_pdf_retriever/{chatbot_id}")
    
#     if not session_id:
#         session_id= "1234default"
    
#     if not question or not session_id:
#         logger.info("Invalid input. Please provide a question and session_id")
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input. Please provide a question, session_id and user_id")
    
#     try:
#         return rag_func(session_id,question,kb_path,db,model) 
#     except HTTPException as e: 
#         logger.info(f'An http error occured: \n {str(e)}')
#         raise e
#     except Exception as e:
#         logger.info(f'An error occured: \n {str(e)}')
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")     



# @router.post("/chat_multiturn")  #fixed this function
# def pdf_qna(input_data:QueryInput, db: Session = Depends(get_db)):
#     question= input_data.question
#     chatbot_id = input_data.chatbot_id
#     token =input_data.token
#     user_id=input_data.user_id
    
#     ##get session id 
#     session_id=SessionRepository.create_or_update_session(db,token,chatbot_id,"session_test1",user_id)
    
#     #get chathistory
    
    
#     print(session_id)
    
#     kb_path=Path(f"./data/uploaded_pdf_retriever/{chatbot_id}")
    
#     if not session_id:
#         session_id= "1234default"
    
#     if not question or not session_id:
#         logger.info("Invalid input. Please provide a question and session_id")
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input. Please provide a question, session_id and user_id")
    
#     try:
#         return StreamingResponse(run_multiturn_doc_chain(session_id,question,kb_path,db), media_type="text/event-stream") 
#     except HTTPException as e: 
#         logger.info(f'An http error occured: \n {str(e)}')
#         raise e
#     except Exception as e:
#         logger.info(f'An error occured: \n {str(e)}')
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")