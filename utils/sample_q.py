from fastapi import APIRouter, Depends, HTTPException
from requests import Session
# from app.models.chatbot import Chatbot
# from app.models.knowdegde_base import KnowledgeBase
# from app.models.user import User
# from app.models.user_chatbot import UserChatbot
# from sqlalchemy.orm import joinedload
# from app.db import engine, SessionLocal, Base, get_db
from utils.helper import model

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader,PyPDFLoader
from langchain_openai import ChatOpenAI
from dotenv import dotenv_values
from langchain_openai import OpenAIEmbeddings
from prompts.generate_sample_question_prompt import template

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        ("human", "{context}"),
    ]
)

output_parser = StrOutputParser()

def get_sample_questions(chatbot_id: int):
    try:
        # paths = db.query(KnowledgeBase.path).filter(KnowledgeBase.chatbot_id == chatbot_id).all()
        # paths= [path[0] for path in paths]  # Extracting paths from the list of tuples
        # # print(paths)
        user_pdf_directory = f"./data/uploaded_pdfs/{chatbot_id}"
        
        #todo replace this with pdf_directory
        loader = PyPDFDirectoryLoader(user_pdf_directory)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        chain=chat_template|model|output_parser
        batch_text=[]
        for text in texts:
            context = text.page_content
            batch_text.append({"context":context})
            
        ans=chain.batch(batch_text)
        
        questions_list=[]
        for i in ans:
            questions=i.strip().split('?')
            for x in range(len(questions)):
                remove_extra_space=questions[x].strip()
                questions[x]=remove_extra_space+'?'
            if questions[-1]=='?':
                questions.pop()
            if len(questions)>6:
                questions=questions[:6]
            for x in questions:        
                questions_list.append(x)     
        
        # print(f"documents: {len(documents)}")
        # print(f"texts:",texts)
        
        return questions_list
        
        
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    try:
        # # Create a database session
        # db = SessionLocal()

        # Call the function to get paths associated with a chatbot
        chatbot_id = 36  # Replace with the desired chatbot ID
        sample_questions=get_sample_questions(chatbot_id)
        
        print(sample_questions)
    except:
        print("Error in Creating Sample Questions")