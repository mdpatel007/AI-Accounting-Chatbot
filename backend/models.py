from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    message: str
    extra: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str

class QueryRequest(BaseModel):
    user_id: str
    query: str
    collection_name: str = "documents"
    top_k: int = 3
    chat_history: Optional[list[dict]] = [] 