# 📄 PDF Chat — RAG Document Assistant

Chat with any PDF using AI. Upload a document and ask questions — get accurate answers with source citations.

![PDF Chat Demo](demo.gif)

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