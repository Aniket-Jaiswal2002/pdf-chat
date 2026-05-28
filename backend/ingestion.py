import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

# Load the embedding model once (downloads on first run ~90MB)
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_path: str) -> str:
    """Open a PDF and extract all text from every page."""
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks.
    Why overlap? So we don't lose context at chunk boundaries.
    Example: chunk_size=500 means each chunk is ~500 characters.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap  # move forward but keep 50 chars overlap
    return chunks

def build_vector_store(chunks: list[str]):
    """
    Convert chunks to embeddings and store in FAISS.
    Embeddings = numbers that represent the meaning of text.
    FAISS = a library that can search those numbers super fast.
    """
    embeddings = model.encode(chunks, show_progress_bar=True)
    embeddings = np.array(embeddings, dtype="float32")

    # Create FAISS index (think of it as a searchable database)
    dimension = embeddings.shape[1]  # size of each embedding vector
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index, embeddings

def save_store(index, chunks: list[str], path: str = "store"):
    """Save FAISS index and chunks to disk so we don't reprocess every time."""
    os.makedirs(path, exist_ok=True)
    faiss.write_index(index, f"{path}/index.faiss")
    with open(f"{path}/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

def load_store(path: str = "store"):
    """Load previously saved FAISS index and chunks from disk."""
    index = faiss.read_index(f"{path}/index.faiss")
    with open(f"{path}/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def ingest_pdf(pdf_path: str):
    """Full pipeline: PDF → text → chunks → embeddings → saved store."""
    print(f"Reading PDF: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)

    print("Chunking text...")
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")

    print("Building vector store...")
    index, embeddings = build_vector_store(chunks)

    print("Saving to disk...")
    save_store(index, chunks)

    print("Done! PDF ingested successfully.")
    return len(chunks)