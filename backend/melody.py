import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # so we can import vector_store from raga/ root
import json

import ollama
from vector_store import retrieve

GROUNDING_SYSTEM_PROMPT = """You are a question-answering assistant for insurance policy documents. Answer the user's question using ONLY the information in the context below.

Internally check: which specific policy terms, figures, or conditions are explicitly stated in the context, and whether the question is about something in that set. Do NOT show this checking process in your response.

If the question asks about anything not explicitly stated in the context, respond with EXACTLY this text and nothing else: "I don't have enough information to answer that."

If the context includes chunks from more than one policy document, always state which policy each fact comes from — for example: "Under [Policy A]: ... Under [Policy B]: ..." Never state a fact as if it applies to "the policy" in general when multiple policies are present in the context.

Otherwise, give a direct final answer only — no reasoning steps, no restating the question, no additional commentary after the answer.

Rules:
- Never cite a source for a claim the source does not actually contain.
- Cite the source for every claim you make, like [source: 1].
- Do not use any outside knowledge under any circumstance."""

def build_prompt(context_chunks, question):
    from collections import defaultdict
    by_policy = defaultdict(list)
    for c in context_chunks:
        by_policy[c.source].append(c.text)
    
    context_sections = []
    for i, (source, texts) in enumerate(by_policy.items(), 1):
        combined = "\n".join(texts)
        context_sections.append(f"=== POLICY {i}: {source} ===\n{combined}")
    
    context_text = "\n\n".join(context_sections)
    
    return f"""Context (grouped by policy document):
{context_text}

Question: {question}

Answer separately for EACH policy shown above, clearly naming which policy each part of your answer refers to. Do not combine information across policies into a single unified statement."""

def ask_grounded(question, temperature=0.1, n_results=3):
    chunks = retrieve(question, n_results=n_results)
    prompt = build_prompt(chunks, question)
    response = ollama.chat(model="phi4-mini", messages=[
        {"role": "system", "content": GROUNDING_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ], options={"temperature": temperature})
    return response["message"]["content"], chunks

REFUSAL_TEXT = "i don't have enough information to answer that"

def is_refusal(answer):
    return REFUSAL_TEXT in answer.lower()
def generate_answer(question: str, temperature: float = 0.1, n_results: int = 3) -> dict:
    answer_text, chunks = ask_grounded(question, temperature=temperature, n_results=n_results)
    return {
        "answer": answer_text,
        "sources": [c.source for c in chunks],
        "refused": is_refusal(answer_text),
    }

if __name__ == "__main__":
    question = "What is the surrender value calculation?"
    from vector_store import retrieve
    chunks = retrieve(question)
    
    print(f"Retrieved {len(chunks)} chunks:\n")
    for c in chunks:
        print(f"[{c.source}] score={c.score:.4f}")
        print(c.text[:200])
        print("---")
    
    answer, chunks = ask_grounded(question)
    print("\nANSWER:", answer)

    

from vector_store import client, collection
print("Chroma client path:", client._system.settings.persist_directory if hasattr(client, '_system') else "unknown")
print("Collection count:", collection.count())
print("All collections:", client.list_collections())