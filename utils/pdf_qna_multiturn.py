import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import AIMessage, HumanMessage
from utils.helper import model, embedding, format_docs, format_docs_list
from prompts.pdf_qa_prompt import qa_system_prompt, re_q_prompt_template
from utils.pdf_utils import load_vector_db
from utils.q_rephrase import contextualized_question_to_str, contextualized_question
from app.repository.session_history_repository import SessionHistoryRepository
from app.db import get_db
from sqlalchemy.orm import Session as SQLASession
from datetime import datetime
from langchain_community.callbacks import get_openai_callback
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, status
from ragas.metrics import answer_relevancy
from ragas import evaluate
import pandas as pd
from datasets import Dataset

from utils.pdf_qna import upload_pdf_chain_call, qa_prompt
# import nest_asyncio
# nest_asyncio.apply()
re_q_prompt = ChatPromptTemplate.from_template(re_q_prompt_template) 

def ask_again(response, question, context):
    re_q_chain = re_q_prompt | model
    answer = re_q_chain.invoke({"context":context, "question":question})
    return answer.content

def calc_confidence_score(payload,llm,embeddings):
    # print(payload)
    payload={'0':payload}
    data_pd = pd.DataFrame.from_dict(payload, orient='index')
    dataset = Dataset.from_pandas(data_pd)
    evaluation = evaluate(
            dataset,
            llm=llm,
            embeddings=embeddings,
            metrics=[answer_relevancy],
            raise_exceptions=False
        )
    return evaluation['answer_relevancy']
    
def make_payload(question,answer,context):
    return {
        "contexts":context,
        "question":question,
        "answer":answer
    }

def revise_response(response, question, context, threshold=0.7):
    payload = make_payload(question, response, context)
    score = calc_confidence_score(payload,model,embedding)
    print("score: ",score)
    if(score<threshold):
        print("score no good. asking again")
        # return "I am sorry, I do not understand you."
        return ask_again(response, question, context)
    else: return response

def stream_string(string, chunk_size=5):
    for i in range(0, len(string), chunk_size):
        chunk = string[i:i + chunk_size]
        yield chunk

class CaptureOutput:
    def __init__(self):
        self.output = None

contextualized_question_str = CaptureOutput()

# def run_multiturn_doc_chain(session_id, question, kb_path, db):
#     vectorstore = load_vector_db(embedding, kb_path)
#     retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
#     chat_history=SessionHistoryRepository.get_history(db,session_id)

#     # contextualized_question_str = contextualized_question_to_str({"question": question, "chat_history": chat_history})
#     rag_chain = (
#                     RunnablePassthrough.assign(context= contextualized_question | retriever | format_docs)
#                     | qa_prompt
#                     | model
#                             )
#     output = ""
#     with get_openai_callback() as cb:
#         start_time = datetime.now()
#         response = rag_chain.invoke({"question": question, "chat_history": chat_history}).content
#         response = revise_response(response,question, format_docs_list(retriever.invoke(question)))

#         for chunk in stream_string(response):
#             output += chunk
#             if len(chunk) > 0:
#                 yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"



#         end_time = datetime.now()
#         elapsed_time = (end_time - start_time).total_seconds()
#         cost = cb.total_cost
#     SessionHistoryRepository.set_history(db,session_id,question,output,cost,elapsed_time)                   
# 
# 
# 


def make_prompt(question, chat_history, context):
    return qa_prompt.format(context=context, question=question, chat_history=chat_history)

def run_multiturn_doc_chain(session_id, question, kb_path, db):
    vectorstore = load_vector_db(embedding, kb_path)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    chat_history=SessionHistoryRepository.get_history(db,session_id)

    contextualized_question_str = contextualized_question_to_str({"question": question, "chat_history": chat_history})
    retrieved_docs = retriever.invoke(contextualized_question_str)
    contexts = format_docs(retrieved_docs)
    # qa_prompt_formatted = make_prompt(contextualized_question_str, chat_history, contexts)
    
    def callable_q(_):
        return contexts
    rag_chain = (
                    RunnablePassthrough.assign(context= callable_q)
                    | qa_prompt
                    | model
                            )
    output = ""
    print(contextualized_question_str)
    with get_openai_callback() as cb:
        start_time = datetime.now()
        response = rag_chain.invoke({"question": question, "chat_history": chat_history}).content
        response = revise_response(response,contextualized_question_str, format_docs_list(retrieved_docs))

        for chunk in stream_string(response):
            output += chunk
            if len(chunk) > 0:
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"



        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        cost = cb.total_cost
    SessionHistoryRepository.set_history(db,session_id,question,output,cost,elapsed_time)            

