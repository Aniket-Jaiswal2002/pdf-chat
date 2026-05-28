from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

from ingestion import ingest_pdf, load_store
from retrieval import retrieve_relevant_chunks
from llm import get_answer

app = FastAPI(title="PDF Chat API")

# Allow React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global store - holds the loaded FAISS index and chunks in memory
store = {"index": None, "chunks": None}

class ChatRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    """Check if the server is running."""
    return {"status": "ok", "pdf_loaded": store["index"] is not None}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Receive a PDF file, save it, run ingestion pipeline.
    After this endpoint, the vector store is ready for questions.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    # Save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Run the full ingestion pipeline
        chunk_count = ingest_pdf(temp_path)
        
        # Load the store into memory for querying
        store["index"], store["chunks"] = load_store()
        
        return {
            "message": "PDF uploaded and processed successfully",
            "chunks": chunk_count,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Always clean up the temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Receive a question, retrieve relevant chunks, get answer from LLM.
    This is the full RAG pipeline in one endpoint.
    """
    if store["index"] is None:
        raise HTTPException(status_code=400, detail="No PDF uploaded yet. Please upload a PDF first.")
    
    # Step 1: Find relevant chunks (Retrieval)
    relevant_chunks = retrieve_relevant_chunks(
        request.question,
        store["index"],
        store["chunks"]
    )
    
    # Step 2: Get answer from LLM using those chunks (Generation)
    answer = get_answer(request.question, relevant_chunks)
    
    # Step 3: Return answer + source chunks so frontend can show citations
    return {
        "answer": answer,
        "sources": [c["chunk"][:200] + "..." for c in relevant_chunks]  # first 200 chars of each source
    }