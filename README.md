# 📄 PDF Chat — RAG Document Assistant

Chat with any PDF using AI. Upload a document and ask questions — get accurate answers with source citations powered by LLaMA 3.3 via Groq.

## ✨ Features

- 📤 Upload any PDF document
- 🔍 Semantic search using vector embeddings
- 🤖 AI-powered answers using LLaMA 3.3 70B
- 📎 Source citations shown for every answer
- ⚡ Fast retrieval with FAISS vector store
- 🎨 Clean React chat interface

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | FastAPI (Python) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | FAISS |
| LLM | Groq + LLaMA 3.3 70B |

## 🧠 How It Works (RAG Pipeline)

1. **Upload** — PDF is parsed and split into overlapping chunks
2. **Embed** — Each chunk is converted to a vector using sentence-transformers
3. **Store** — Vectors are indexed in FAISS for fast similarity search
4. **Query** — User question is embedded and matched against chunks
5. **Generate** — Top chunks + question are sent to LLaMA 3.3 via Groq
6. **Respond** — Answer is returned with source citations

## 📁 Project Structure
pdf-chat/
├── backend/
│   ├── main.py          # FastAPI endpoints (/upload, /chat, /health)
│   ├── ingestion.py     # PDF parsing + chunking + embedding
│   ├── retrieval.py     # FAISS similarity search
│   ├── llm.py           # Groq LLM integration + prompt builder
│   └── requirements.txt
├── frontend/
│   └── src/
│       └── App.jsx      # React chat UI with upload + citations
├── .gitignore
└── README.md

## ⚙️ Run Locally

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API key (free at https://console.groq.com)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Create .env file
echo GROQ_API_KEY=your_key_here > .env

uvicorn main:app --reload
```

Backend runs at http://127.0.0.1:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

## 🔑 Environment Variables

Create `backend/.env`:
GROQ_API_KEY=your_groq_api_key_here

Get a free API key at https://console.groq.com

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Check server status |
| POST | /upload | Upload and process a PDF |
| POST | /chat | Ask a question about the PDF |

## 🛠️ Built With

- [FastAPI](https://fastapi.tiangolo.com/) — Python web framework
- [sentence-transformers](https://www.sbert.net/) — Text embeddings
- [FAISS](https://github.com/facebookresearch/faiss) — Vector similarity search
- [Groq](https://console.groq.com) — LLM inference API
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF parsing
- [React](https://react.dev/) — Frontend UI