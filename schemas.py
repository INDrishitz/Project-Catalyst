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

# --- Add this to the bottom of schemas.py ---

class MetricsResponse(BaseModel):
    """Format guaranteed to Person D for the Observability Dashboard"""
    total_queries: int
    average_faithfulness: float
    average_retrieval_precision: float
    system_uptime_seconds: float