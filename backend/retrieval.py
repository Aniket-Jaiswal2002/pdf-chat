from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Use the same model as ingestion - must match!
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_chunks(query: str, index, chunks: list[str], top_k: int = 3) -> list[dict]:
    """
    Given a user question, find the most relevant chunks from the PDF.
    
    How it works:
    1. Convert the question into an embedding (numbers)
    2. Search FAISS for the closest matching chunk embeddings
    3. Return the top_k most relevant chunks with their scores
    """
    # Convert question to embedding
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding, dtype="float32")

    # Search FAISS - returns distances and indices of closest chunks
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:  # -1 means no result found
            results.append({
                "chunk": chunks[idx],
                "score": float(distances[0][i]),
                "index": int(idx)
            })

    return results