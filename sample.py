'''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define what incoming data must look like
class ChatRequest(BaseModel):
    query: str

# Define your API endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    # Month 1: Return mock data so the frontend can build their UI
    return {
        "answer": f"Echoing your query: {request.query}",
        "sources": ["source_1.pdf", "source_2.pdf"],
        "faithfulness_score": 0.95
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}'''

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "Welcome to my FastAPI"}

@app.post("/chat")
def chat(request: ChatRequest):
    return {
        "answer": f"Echoing your query: {request.query}",
        "sources": ["source_1.pdf", "source_2.pdf"],
        "faithfulness_score": 0.95
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}