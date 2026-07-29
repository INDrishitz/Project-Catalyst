from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatRequest, ChatResponse
from typing import Dict, List
import time
import logging

# --- Logging Configuration ---
# This saves logs to a file AND prints them to your terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("api_logs.log"),
        logging.StreamHandler()
    ]
)
# -----------------------------

app = FastAPI(title="Agentic RAG Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions_db: Dict[str, List[dict]] = {}
MAX_HISTORY_MESSAGES = 6

@app.get("/health")
def health_check():
    logging.info("Health check endpoint pinged.")
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id
    start_time = time.time()  # Start the stopwatch
    
    logging.info(f"Incoming request | Session: {session_id} | Query: '{request.query}'")
    
    try:
        if session_id not in sessions_db:
            sessions_db[session_id] = []
            
        history = sessions_db[session_id]
        
        # Simulate AI processing time
        time.sleep(1)
        
        history_length = len(history)
        mock_answer = f"Mock Answer. (Session '{session_id}' has {history_length} past messages)."
        
        history.append({"role": "user", "content": request.query})
        history.append({"role": "assistant", "content": mock_answer})
        
        if len(history) > MAX_HISTORY_MESSAGES:
            sessions_db[session_id] = history[-MAX_HISTORY_MESSAGES:]
            
        # Calculate exactly how long the request took
        process_time = time.time() - start_time
        logging.info(f"Success | Session: {session_id} | Latency: {process_time:.4f} seconds")
        
        return ChatResponse(
            answer=mock_answer,
            citations=["[cite: 1]"],
            sources=["mock_doc.pdf"],
            faithfulness_score=0.98
        )
        
    except Exception as e:
        process_time = time.time() - start_time
        # Log the exact error so you don't have to guess why it crashed
        logging.error(f"Failed | Session: {session_id} | Error: {str(e)} | Latency: {process_time:.4f} seconds")
        raise HTTPException(status_code=500, detail="Internal Server Error")