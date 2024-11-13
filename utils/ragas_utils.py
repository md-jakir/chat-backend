from langchain_community.document_loaders import PyPDFLoader
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import dotenv_values
from datasets import Dataset
from utils.logger import logger
import httpx
import os
# import openai
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
)
from ragas import evaluate
from ragas.integrations.langchain import EvaluatorChain as RagasEvaluatorChain
import nest_asyncio
nest_asyncio.apply()

config = dotenv_values(".env")
openai_api_key=config['OPENAI_API_KEY'] 



def load(file):
    loader = PyPDFLoader(file, extract_images=True)
    documents = loader.load()
    for document in documents:
        document.metadata['filename'] = document.metadata['source']
    return documents

# Initialize an empty dictionary to store the results
async def dataset_generator(questions,chatbot_id, token, model_id):
    endpoint_url = "http://127.0.0.1:8000/api/chatbot/chat_aws"

    payload_template = {
        "chatbot_id": chatbot_id,
        "token": token,
        "model_id": model_id
    }
    results = {}
    async with httpx.AsyncClient() as client:
        for idx, question in enumerate(questions, start=1):
            print(f"{idx}: {question}")
            # Prepare the payload with the current question
            payload = payload_template.copy()
            payload["question"] = question
            
            try:
                # Send the POST request to the endpoint
                response = await client.post(endpoint_url, json=payload)
                # Check if the request was successful
                if response.status_code == 200:
                    # Parse the response JSON
                    response_data = response.json()
                    # Store the result in the dictionary
                    results[idx] = {
                        "question": question,
                        "answer": response_data.get("answer", ""),
                        "ground_truth": response_data.get("answer", ""),
                        "contexts": response_data.get("context", "")
                    }
                else:
                    # Handle the case where the request failed
                    results[idx] = {
                        "question": question,
                        "answer": "Request failed with status code {}".format(response.status_code),
                        "ground_truth": "",
                        "contexts": [""]
                    }
            except Exception as e:
                # Handle any exceptions that occur during the request
                results[idx] = {
                    "question": question,
                    "answer": "An error occurred >_< : {}".format(str(e)),
                    "ground_truth": "",
                    "contexts": [""]
                }

    return results

def evaluate_rag(chatbot_id,dataset,model,embedding,metrics=[
                context_precision,
                faithfulness,
                answer_relevancy,
                context_recall,
            ]):
    logger.info(f'starting evaluation')
    # dataset = generate(file)
    evaluation = evaluate(
            dataset,
            metrics=metrics,
            llm=model,
            embeddings=embedding,
            raise_exceptions=False
        )
    logger.info(f'evaluation completed')
    logger.info(f'writing evaluation to json')
    if not os.path.exists(f'data/rag_evaluation_reports/{chatbot_id}'):
        os.makedirs(f'data/rag_evaluation_reports/{chatbot_id}')
    evaluation.to_pandas().to_json(f'data/rag_evaluation_reports/{chatbot_id}/evaluation.json',orient='index')
