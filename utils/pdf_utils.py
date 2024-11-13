import os
from datetime import datetime
from fastapi import UploadFile
from typing import List
from langchain_community.vectorstores import FAISS
from pathlib import Path
from fastapi import  HTTPException
from utils.helper import embedding
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from utils.logger import logger

def uploaded_pdf_to_retriever(file_path: str, chatbot_id: int = None):  #chatbot_id added
    embedding_function = embedding
    persist_directory = Path(f"./data/uploaded_pdf_retriever/{chatbot_id}")
    
    logger.info(f"Loading, chunking, and indexing the contents of the PDF: {file_path}...")
    # loader = PyPDFDirectoryLoader(file_path, extract_images=True)
    loader = PyPDFDirectoryLoader(file_path)
   
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # Create the persist directory and save to disk
    persist_directory.mkdir(parents=True, exist_ok=True)
    db = FAISS.from_documents(texts, embedding_function)
    db.save_local(str(persist_directory))
    logger.info("Database saved to disk and loaded successfully!")

    return db


async def process_uploaded_pdfs(files: List[UploadFile], chatbot_id: int = None):
    user_pdf_directory = f"./data/uploaded_pdfs/{chatbot_id}"           #chatbot_id added
    os.makedirs(user_pdf_directory, exist_ok=True)

    # # Remove all existing PDF files in the directory
    # for filename in os.listdir(user_pdf_directory):
    #     file_path = os.path.join(user_pdf_directory, filename)
    #     if filename.endswith(".pdf"):
    #         try:
    #             os.remove(file_path)
    #         except Exception as e:
    #             logger.info(f"Failed to delete {file_path}. Reason: {e}")
    all_files_location = []
    # Read the uploaded files            
    for file in files:
        safe_file_name = "".join(char for char in file.filename if char.isalnum() or char in "._-")
        safe_file_name = safe_file_name[:-4]  # Remove extension
        file_extension = file.filename.split('.')[-1]
        file_location = os.path.join(user_pdf_directory, f"{safe_file_name}.{file_extension}")
        # Save the uploaded file
        with open(file_location, "wb") as out_file:
            content = await file.read() 
            out_file.write(content)
        logger.info(f"File {safe_file_name}.{file_extension} uploaded successfully.")

        if(chatbot_id):
            all_files_location.append({
                "path": file_location,
                "chatbot_id": chatbot_id
            })
        
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_file_path = os.path.join(os.getcwd(), "last_update_timestamp.txt")
    with open(timestamp_file_path, "a") as timestamp_file:
        timestamp_file.write(f"{timestamp}: Updated PDF files.\n")
    
    uploaded_pdf_to_retriever(user_pdf_directory,chatbot_id) #chatbot_id added   
    return {
        "root_path": user_pdf_directory,
        "files": all_files_location
    }
    
def load_vector_db(embedding_function, kb_path):
    persist_directory = kb_path #Path(f"./data/uploaded_pdf_retriever")
    logger.info(persist_directory)
    if persist_directory.exists():
        logger.info(f"Loading Uploaded PDF FAISS database from disk (Directory: {persist_directory})...")
        db = FAISS.load_local(str(persist_directory), embedding_function, allow_dangerous_deserialization=True)
        logger.info("Database loaded successfully!")
        return db
    else:
        raise HTTPException(status_code=404, detail="FAISS database not found for the specified file name")    
