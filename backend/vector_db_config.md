# Vector DB Configuration — for Person C

**Database:** ChromaDB (local/persistent, not a separate server currently)

**Storage:**
- Currently using `chromadb.PersistentClient(path="./chroma_db")`
- Data lives on disk at `raga/chroma_db/` — needs a persistent volume mount in Docker so data survives container restarts

**Networking:**
- Right now, ChromaDB runs embedded inside my Python process (no separate network port)
- For docker-compose, this likely means: my ingestion/retrieval service just needs a mounted volume for `chroma_db/`, not a separate network service — unless we later switch to ChromaDB's client-server mode (a separate container with its own port, e.g. 8000)

**Question for the team:** do we want ChromaDB embedded in my service (simpler, current setup) or running as its own container (needed if multiple services need direct DB access)? This affects the docker-compose structure.

**Collection name:** `raga_docs`
**Embedding dimensions:** 1024 (BGE-M3 dense vectors)