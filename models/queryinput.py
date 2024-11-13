from pydantic import BaseModel

class QueryInput(BaseModel):
    question: str
    session_id: str
    chatbot_id: str