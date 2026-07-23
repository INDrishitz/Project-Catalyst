from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatRequest, ChatResponse
import time

app = FastAPI(title="Agentic RAG Backend")

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you would replace "*" with the frontend's exact URL
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)
# --------------------------

@app.get("/health")
def health_check():
    """Health check endpoint for cloud deployment and testing."""
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Month 1 Mock Endpoint"""
    time.sleep(1) 
    return ChatResponse(
        answer=f"This is a mock answer mimicking the LLM. You asked: '{request.query}'",
        citations=["[cite: 1]"],
        sources=["mock_document.pdf"],
        faithfulness_score=0.99
    )