from pathlib import Path
from dataclasses import dataclass
import chromadb
from FlagEmbedding import BGEM3FlagModel

CLEAN_DIR = Path(__file__).parent.parent / "data" / "clean_txts"

model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
client = chromadb.PersistentClient(path=str(Path(__file__).parent.parent / "chroma_db"))
collection = client.get_or_create_collection("raga_docs")


@dataclass
class Chunk:
    text: str
    source: str
    score: float


def embed(texts: list[str]) -> list[list[float]]:
    output = model.encode(texts, return_dense=True, return_sparse=False)
    return output["dense_vecs"].tolist()


def ingest_chunks(chunks: list[str], sources: list[str]):
    """Embed and store chunks in ChromaDB."""
    vectors = embed(chunks)
    ids = [f"{sources[i]}_{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=vectors,
        metadatas=[{"source": s} for s in sources],
        ids=ids,
    )
    print(f"Ingested {len(chunks)} chunks into ChromaDB.")


def retrieve(query: str, n_results: int = 3) -> list[Chunk]:
    """THE CONTRACT — this signature must not change without updating CONTRACTS.md
    and telling Person C."""
    query_vec = embed([query])[0]
    results = collection.query(query_embeddings=[query_vec], n_results=n_results)

    chunks = []
    for text, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        chunks.append(Chunk(text=text, source=meta["source"], score=1 - dist))
    return chunks


if __name__ == "__main__":
    # quick smoke test using whatever's in clean_txts/
    files = list(CLEAN_DIR.glob("*.txt"))
    if not files:
        print("Run parse_documents.py first.")
    else:
        all_chunks, all_sources = [], []
        for f in files:
            text = f.read_text(encoding="utf-8")
            # naive split for this smoke test — use chunking_experiments.py's
            # recursive_chunks() for the real pipeline
            pieces = [text[i:i+1000] for i in range(0, len(text), 1000)]
            all_chunks.extend(pieces)
            all_sources.extend([f.name] * len(pieces))

        ingest_chunks(all_chunks, all_sources)

        test_query = "example query related to your documents"
        results = retrieve(test_query)
        for r in results:
            print(f"[{r.source}] score={r.score:.3f}\n{r.text[:150]}...\n")