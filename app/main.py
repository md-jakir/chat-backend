from typing import List
from fastapi import FastAPI, File, HTTPException, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from pathlib import Path

from app.db import Base, engine
from app.endpoints import user_controller
from models.queryinput import QueryInput
from utils.pdf_utils import process_uploaded_pdfs
from utils.pdf_qna import upload_pdf_chain_call
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import logger
from app.helpers.helper import http_error_handler
from fastapi.exceptions import RequestValidationError
from app.helpers.custom_exception_handler import validation_exception_handler
from fastapi.staticfiles import StaticFiles

app = FastAPI()

from app.endpoints import user_controller
from app.endpoints import auth_controller
from app.endpoints import admin_controller
from app.endpoints import chatbot_controller
from app.endpoints import user_chatbot_controller
from app.endpoints import sample_qustion_controller
from app.endpoints import knowledge_base_controller
from app.endpoints import session_controller
from app.endpoints import analytics_controller
from app.endpoints import prompt_controller
from app.endpoints import widget_controller
from app.endpoints import session_history_controller
from app.endpoints import whatsapp_chat_controller

from app.endpoints import evaluate_controller

sessions = {}

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_controller.router, prefix="/api/user", tags=["User"])
app.include_router(auth_controller.router, prefix="/api/auth", tags=["Auth"])
app.include_router(admin_controller.router, prefix="/api/admin", tags=["Admin"])
app.include_router(chatbot_controller.router, prefix="/api/chatbot", tags=["Chatbot"])
app.include_router(user_chatbot_controller.router, prefix="/api/user-chatbot", tags=["UserChatbot"])
app.include_router(sample_qustion_controller.router, prefix="/api/sample-qustion", tags=["SampleQustion"])
app.include_router(knowledge_base_controller.router, prefix="/api/knowledge-base", tags=["KnowledgeBase"])
app.include_router(session_controller.router, prefix="/api/session", tags=["Session"])
app.include_router(analytics_controller.router,prefix="/api/analytics", tags=["Analytics"])
app.include_router(prompt_controller.router,prefix="/api/prompt", tags=["Prompt"])
app.include_router(widget_controller.router, prefix="/api/widget", tags=["Widget"])
app.include_router(session_history_controller.router, prefix="/api/session-history", tags=["SessionHistory"])
app.include_router(evaluate_controller.router, prefix="/api/evaluate", tags=["Evaluate"])
app.include_router(whatsapp_chat_controller.router, prefix="/api/whatsapp-chat", tags=["WhatsappChat"]) 

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


#Health Checker
@app.get("/")
async def health():
    logger.info("Health check requested")
    return {"Status": "Ok 201"}


@app.post("/upload_pdf")
async def upload_pdf(files: List[UploadFile] = File(...)):
    await process_uploaded_pdfs(files)

    return {
        "message": "PDFs uploaded successfully and retrievers created",
        "filenames": [file.filename for file in files]
    }


@app.post("/api/chat")
async def upload_pdf_qa(input_data:QueryInput):
    question= input_data.question
    session_id= input_data.session_id
    chatbot_id=input_data.chatbot_id #chatbot id added
    
    kb_path=Path(f"./data/uploaded_pdf_retriever/{chatbot_id}")
    
    if not session_id:
        session_id= "1234default"
    
    if not question or not session_id:
        logger.info("Invalid input. Please provide a question and session_id")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input. Please provide a question, session_id and user_id")
    
    try:
        return StreamingResponse(upload_pdf_chain_call(sessions,session_id,question,kb_path), media_type="text/event-stream") 
    except HTTPException as e: 
        logger.info(f'An http error occured: \n {str(e)}')
        raise e
    except Exception as e:
        logger.info(f'An error occured: \n {str(e)}')
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# listen the app on port 8000
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=5000)