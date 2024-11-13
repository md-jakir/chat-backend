from langchain_openai import ChatOpenAI
from dotenv import dotenv_values
from langchain_openai import OpenAIEmbeddings
import boto3
import json
import os

from langchain_community.chat_models import BedrockChat
from langchain_community.embeddings import BedrockEmbeddings


# config = dotenv_values(".env")
# openai_api_key=config['OPENAI_API_KEY'] 
# key=config['key']
# secret=config['secret']
# session_token=config['session_token']


openai_api_key = os.getenv("OPENAI_API_KEY")
key = os.getenv("key")
secret = os.getenv("secret")
session_token = os.getenv("session_token")



model = ChatOpenAI(
    model_name="gpt-4o-mini",
    streaming=True,
    temperature=0.05, 
    api_key=openai_api_key
)

embedding = OpenAIEmbeddings(api_key=openai_api_key,model='text-embedding-3-small')

def format_docs(documents):
    # print(documents)
    return "\n\n".join(doc.page_content for doc in documents)

def format_docs_list(documents):
    return [doc.page_content for doc in documents]
def text_streamer(msg):
    words = msg.split(' ')
    for word in words:
        word= word+' '
        yield f'data: {json.dumps(word, ensure_ascii=False)}\n\n'


session = boto3.session.Session(
    aws_access_key_id=key,
    aws_secret_access_key=secret,
    aws_session_token=session_token
)

bedrock = session.client('bedrock-runtime',region_name="us-east-1")

# model_id_llama_3_70b="meta.llama3-70b-instruct-v1:0"
# model_id_mistral_7b="mistral.mistral-7b-instruct-v0:2"

# model_kwargs =  { 
#     "temperature": 0.05,
# }

# model_mistral_7b = ChatBedrock(
#     model_id=model_id_mistral_7b,
#     model_kwargs=dict(temperature=0),
#     client=bedrock,
#     streaming=True
# )