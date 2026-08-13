from fastapi import FastAPI, HTTPException
from schemas import ChatRequest, ChatResponse, MetricsResponse
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatRequest, ChatResponse
from typing import Dict, List
import time
import logging

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("api_logs.log"),
        logging.StreamHandler()
    ]
)

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
SERVER_START_TIME = time.time()  # New variable to track uptime

@app.get("/health")
def health_check():
    logging.info("Health check endpoint pinged.")
    return {"status": "healthy"}


@app.get("/metrics", response_model=MetricsResponse)
def get_metrics():
    """
    Month 4/6 Task: Exposes evaluation metrics for the frontend dashboard.
    Currently returns mock RAGAS scores until Person B integrates real evals.
    """
    uptime = time.time() - SERVER_START_TIME
    
    logging.info("Metrics endpoint pinged by frontend dashboard.")
    
    # Returning mock data representing Person B's future evaluation results
    return MetricsResponse(
        total_queries=150,
        average_faithfulness=0.92,
        average_retrieval_precision=0.88,
        system_uptime_seconds=round(uptime, 2)
    )

# ---------------------------------------------------------
# NEW FUNCTION: The Query Rewriter (Month 3 Task)
# Notice how this sits OUTSIDE and ABOVE the chat endpoint!
# ---------------------------------------------------------
def rewrite_query(current_query: str, history: List[dict]) -> str:
    """Analyzes history and rewrites query for the retrieval engine."""
    if not history:
        return current_query
        
    logging.info(f"Original Query: {current_query}")
    rewritten = f"[Rewritten based on history] {current_query}"
    logging.info(f"Rewritten Query: {rewritten}")
    
    return rewritten


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id
    start_time = time.time()
    
    logging.info(f"Incoming request | Session: {session_id} | Query: '{request.query}'")
    
    try:
        # 1. Initialize or fetch history
        if session_id not in sessions_db:
            sessions_db[session_id] = []
        history = sessions_db[session_id]
        
        # ---------------------------------------------------------
        # NEW LOGIC: We call the rewriter right here!
        # ---------------------------------------------------------
        search_query = rewrite_query(request.query, history)
        
        # Simulate AI processing time
        time.sleep(1)
        
        # We now use the 'search_query' in our mock answer
        history_length = len(history)
        mock_answer = f"Mock Answer based on search: '{search_query}'. (Session '{session_id}' has {history_length} past messages)."
        
        # Update history
        history.append({"role": "user", "content": request.query})
        history.append({"role": "assistant", "content": mock_answer})
        
        if len(history) > MAX_HISTORY_MESSAGES:
            sessions_db[session_id] = history[-MAX_HISTORY_MESSAGES:]
            
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
        logging.error(f"Failed | Session: {session_id} | Error: {str(e)} | Latency: {process_time:.4f} seconds")
        raise HTTPException(status_code=500, detail="Internal Server Error")