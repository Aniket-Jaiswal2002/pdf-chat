from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
import os

from ingestion import ingest_pdf, load_store
from retrieval import retrieve_relevant_chunks
from llm import get_answer

app = FastAPI(title="PDF Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = {"index": None, "chunks": None}

class ChatRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok", "pdf_loaded": store["index"] is not None}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        chunk_count = ingest_pdf(temp_path)
        store["index"], store["chunks"] = load_store()
        return {"message": "PDF uploaded and processed successfully", "chunks": chunk_count, "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/chat")
async def chat(request: ChatRequest):
    if store["index"] is None:
        raise HTTPException(status_code=400, detail="No PDF uploaded yet.")
    relevant_chunks = retrieve_relevant_chunks(request.question, store["index"], store["chunks"])
    answer = get_answer(request.question, relevant_chunks)
    return {"answer": answer, "sources": [c["chunk"][:200] + "..." for c in relevant_chunks]}