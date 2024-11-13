from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from prompts.greetings_prompt import greeting_response_template
from utils.helper import model
import json

greet_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", greeting_response_template),
        ("human", "{question}"),
    ]
)

greet_q_chain = greet_prompt | model| StrOutputParser()



def greet_chain(question):
    for chunk in greet_q_chain.stream({"question": question}):
            chunk_content=chunk
            if len(chunk_content) > 0:
                yield f"data: {json.dumps(chunk_content, ensure_ascii=False)}\n\n"

def greet_chain_call(question):
    return greet_q_chain.invoke({"question": question})    