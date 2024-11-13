from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from fastapi import FastAPI, File, HTTPException, UploadFile, status, Request, Form
from typing import List
# from app.test import dataset_generator
# from utils.ragas_utils import *
import pandas as pd
from datasets import Dataset
import os
from utils.helper import model, embedding
from app.db import get_db
from app.repository.sample_questions_repository import SampleQuestionsRepository

router = APIRouter()

@router.post("/evaluate_rag")
async def upload_pdf_rag( chatbot_id: str , token: str , model_id: str , db: Session = Depends(get_db)):
    #Load sample questions from db
    questions = SampleQuestionsRepository.get_history(db, chatbot_id)

    #prepare dataset
    data = await dataset_generator(questions,chatbot_id,token,model_id)
    data_pd = pd.DataFrame.from_dict(data, orient='index')
    dataset = Dataset.from_pandas(data_pd)
    evaluate_rag(chatbot_id,dataset,model,embedding)
    # return val


    return {
        "message": "PDFs uploaded successfully and reports created",
    }