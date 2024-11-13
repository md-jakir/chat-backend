import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import AIMessage, HumanMessage
from utils.helper import model, embedding, format_docs
from prompts.pdf_qa_prompt import qa_system_prompt
from utils.pdf_utils import load_vector_db
from utils.q_rephrase import contextualized_question
from app.repository.session_history_repository import SessionHistoryRepository
from app.db import get_db
from sqlalchemy.orm import Session as SQLASession
from datetime import datetime
from langchain_community.callbacks import get_openai_callback
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, status
from app.models.prompt import Prompt
from utils.logger import logger
from pathlib import Path
from langdetect import detect
from sqlalchemy.orm import Session
from utils.classify_routes import classify_routes
from utils.greetings import greet_chain_call

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

pre_instruction = """
Follow these instructions strictly. DO NOT answer anything outside of these rules:

"""

context_section = '''

The context (delimited by <context></context>) is given below:
<context>
{context}
</context>

-Strictly answer in the user's language ({target_language}) even if the context is in a different language.
'''


def upload_pdf_chain_call(session_id, question, kb_path, db, chatbot_id, model,detected_lang): 
        pdf_db=load_vector_db(embedding, kb_path)
        retriever = pdf_db.as_retriever(search_type="similarity", search_kwargs={"k": 10})
        
        template=db.query(Prompt.prompt_text).filter(Prompt.chatbot_id==chatbot_id).first()
        
        prompt_val = template
        
        if template:
            logger.info("Template found")
            # prompt_val = pre_instruction + template[0] + context_section
            prompt_val = "".join((pre_instruction, template[0], context_section))
            logger.info(f"Prompt value: {prompt_val}")
        
            qa_prompt_from_db = ChatPromptTemplate.from_messages(
                [
                    ("system", prompt_val),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{question}"),
                ]
            )
        else: 
            qa_prompt_from_db = ChatPromptTemplate.from_messages(
                [
                    ("system", qa_system_prompt),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{question}"),
                ]
            )

        # logger.info(f"Prompt final value: {qa_prompt_from_db}")

        rag_chain = (
                    RunnablePassthrough.assign(context= contextualized_question | retriever | format_docs)
                    | qa_prompt_from_db
                    | model
                            )
        chat_history=SessionHistoryRepository.get_history(db,session_id)
        
        
        # user_session = sessions.setdefault(session_id, {"last_question": None, "conversations": []})
        # for conv in (user_session["conversations"]):
        #     chat_history.extend([HumanMessage(content=conv["question"]), (AIMessage(content=conv["qa_result"]))])
        output=""
        print("Chat history",chat_history)
        
        with get_openai_callback() as cb:
            start_time = datetime.now()
            for chunk in rag_chain.stream({"question": question, "chat_history": chat_history,"target_language":detected_lang}):
                output+=chunk.content
                #   yield chunk.content 
                chunk_content=chunk.content
                if len(chunk_content) > 0:
                            yield f"data: {json.dumps(chunk_content, ensure_ascii=False)}\n\n"  
            # Record the end time
            end_time = datetime.now()
            elapsed_time = (end_time - start_time).total_seconds()
            cost = cb.total_cost
        SessionHistoryRepository.set_history(db,session_id,question,output,cost,elapsed_time)    
        
        
async def upload_pdf_chain_call_whatsapp(session_id: int, question: str, chatbot_id: str,db: Session = Depends(get_db)):
        route=classify_routes(question)
    
        if route == "prompt_injection":
            logger.info(f"Prompt injection detected. Ignoring the above directions and doing something else.")
            return "For security reasons, I can't perform that action. Please ensure your queries are relevant to our conversation topic. Thank you!"
        elif route == "hi":
            logger.info(f"Answering From hi route")
            return greet_chain_call(question)
        elif route == "bye":
            logger.info(f"Answering From bye route")
            return greet_chain_call(question)
        
        kb_path=Path(f"./data/uploaded_pdf_retriever/{chatbot_id}")
        pdf_db=load_vector_db(embedding, kb_path)
        detected_lang=detect(question)
                
        retriever = pdf_db.as_retriever(search_type="similarity", search_kwargs={"k": 10})
        qa_prompt_from_db = ChatPromptTemplate.from_messages(
                [
                    ("system", qa_system_prompt),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{question}"),
                ]
            )
        rag_chain = (
                    RunnablePassthrough.assign(context= contextualized_question | retriever | format_docs)
                    | qa_prompt_from_db
                    | model
        )
        
        chat_history=SessionHistoryRepository.get_history(db,session_id)
        
        ans=rag_chain.invoke({"question": question, "chat_history": chat_history,"target_language":detected_lang})
        
        SessionHistoryRepository.set_history(db,session_id,question,ans.content,0,0)
         
        return ans.content
        
         
                
                           
        # user_session["conversations"].append({"question": question, "qa_result": output})         
        
# def upload_pdf_chain_call_aws(session_id, question, kb_path, db,model): 
#         pdf_db=load_vector_db(embedding, kb_path)
#         retriever = pdf_db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

#         rag_chain = (
#                     RunnablePassthrough.assign(context= contextualized_question | retriever | format_docs)
#                     | qa_prompt
#                     | model
#                             )
#         chat_history=SessionHistoryRepository.get_history(db,session_id)

#         output=""
#         print("Chat history",chat_history)

#         with get_openai_callback() as cb:
#             start_time = datetime.now()
#             for chunk in rag_chain.stream({"question": question, "chat_history": chat_history}):
#                 output+=chunk.content
#                 #   yield chunk.content 
#                 chunk_content=chunk.content
#                 if len(chunk_content) > 0:
#                             yield f"data: {json.dumps(chunk_content, ensure_ascii=False)}\n\n"  
#             # Record the end time
#             end_time = datetime.now()
#             elapsed_time = (end_time - start_time).total_seconds()
#             cost = cb.total_cost
        
#         SessionHistoryRepository.set_history(db,session_id,question,output,cost,elapsed_time)                       
        # user_session["conversations"].append({"question": question, "qa_result": output})         
        
# def rag_func(session_id, question, kb_path, db,model): 
#         pdf_db=load_vector_db(embedding, kb_path)
#         retriever = pdf_db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

#         rag_chain = (
#                     RunnablePassthrough.assign(context= contextualized_question | retriever | format_docs)
#                     | qa_prompt
#                     | model
#                             )
#         chat_history=[]
        
#         context=retriever.invoke(question)
#         context="\n\n".join(doc.page_content for doc in context) 
#         # user_session = sessions.setdefault(session_id, {"last_question": None, "conversations": []})
#         # for conv in (user_session["conversations"]):
#         #     chat_history.extend([HumanMessage(content=conv["question"]), (AIMessage(content=conv["qa_result"]))])
#         # output=""
#         answer=rag_chain.invoke({"question": question, "chat_history": chat_history})
#         print(answer)
        
#         return {
            
#             "question":question,
#             "answer":answer.content,
#             "context":context
#         }
#         # with get_openai_callback() as cb:
#         #     start_time = datetime.now()
#         #     for chunk in rag_chain.stream({"question": question, "chat_history": chat_history}):
#         #         output+=chunk.content
#         #         #   yield chunk.content 
#         #         chunk_content=chunk.content
#         #         if len(chunk_content) > 0:
#         #                     yield f"data: {json.dumps(chunk_content, ensure_ascii=False)}\n\n"  
#         #     # Record the end time
#         #     end_time = datetime.now()
#         #     elapsed_time = (end_time - start_time).total_seconds()
#         #     cost = cb.total_cost
        
#         # SessionHistoryRepository.set_history(db,session_id,question,output,cost,elapsed_time)                       
#         # user_session["conversations"].append({"question": question, "qa_result": output})         
        
                