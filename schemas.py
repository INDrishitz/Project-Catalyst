from pydantic import BaseModel
from typing import List

# --- Internal Formats (From Teammates) ---

class Chunk(BaseModel):
    """Format required from Person A (Retrieval)"""
    text: str
    source: str
    score: float

class Answer(BaseModel):
    """Format required from Person B (LLM)"""
    text: str
    citations: List[str]
    faithfulness_score: float

# --- External Formats (For Frontend) ---

class ChatRequest(BaseModel):
    """Format expected from Person D (Frontend)"""
    query: str

class ChatResponse(BaseModel):
    """Format guaranteed to Person D (Frontend)"""
    answer: str
    citations: List[str]
    sources: List[str]
    faithfulness_score: float