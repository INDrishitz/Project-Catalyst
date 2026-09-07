from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str

class SourceChunk(BaseModel):
    text: str
    source: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    faithfulness_score: Optional[float] = None