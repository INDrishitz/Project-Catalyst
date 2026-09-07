from fastapi import FastAPI
from schemas import ChatRequest, ChatResponse, SourceChunk
from vector_store import retrieve, ingest_chunks

app = FastAPI(title="RAG Platform API")

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    # 1. Call Person A's function to search the ChromaDB vector store
    try:
        raw_chunks = retrieve(request.query)
    except Exception as e:
        return ChatResponse(
            answer=f"Retrieval error: {str(e)}. Did Person A ingest documents yet?", 
            sources=[]
        )
    
    # 2. Map Person A's data shape to your agreed JSON contract
    api_sources = [
        SourceChunk(text=c.text, source=c.source, score=c.score)
        for c in raw_chunks
    ]
    
    # 3. Mock the LLM generation (until Person B delivers their script)
    mock_answer = f"I retrieved {len(api_sources)} chunks for your query. Waiting on Person B for LLM integration."
    
    return ChatResponse(
        answer=mock_answer,
        sources=api_sources,
        faithfulness_score=None
    )