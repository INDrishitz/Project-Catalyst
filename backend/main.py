from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from melody import generate_answer  # Import Person B's function

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat(request: ChatRequest):
    # Call the LLM instead of returning the hardcoded placeholder
    response_data = generate_answer(request.query)
    
    return {
        "answer": response_data["answer"],
        "sources": response_data["sources"]
    }