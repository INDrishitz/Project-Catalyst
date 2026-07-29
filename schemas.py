from pydantic import BaseModel
from typing import List

# --- Updated Request Schema ---
class ChatRequest(BaseModel):
    query: str
    session_id: str  # Tracks unique user chat sessions

class ChatResponse(BaseModel):
    answer: str
    citations: List[str]
    sources: List[str]
    faithfulness_score: float