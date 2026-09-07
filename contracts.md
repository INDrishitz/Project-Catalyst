## retrieve() — owned by Person A

```python
def retrieve(query: str, n_results: int = 3) -> List[Chunk]

class Chunk:
    text: str      # the chunk content
    source: str    # filename or doc identifier, for UI citations
    score: float   # similarity score, higher = more relevant
```

Last updated: [today's date]
Status: mock/stub — real ChromaDB-backed version in progress (Phase 1)