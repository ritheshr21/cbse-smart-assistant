# CBSE Smart Assistant

A RAG-based study assistant for CBSE/NCERT textbooks. Ask questions grounded in the actual textbook content, generate topic-wise MCQ quizzes, and get CBSE-style evaluation of written answers — with weak-topic tracking across sessions.

Currently indexed: **NCERT Class 10 Science**.

## Features

- **Ask a question** — retrieval-augmented answers cited to source textbook excerpts (with links to the source PDF).
- **Generate a quiz** — topic-driven MCQ generation, scored instantly.
- **Evaluate an answer** — free-text answers graded against a CBSE-style marking scheme (score out of 5).
- **Weak-topic tracking** — aggregates evaluation results to surface topics you're struggling with and suggests what to revise.

## Architecture

```
PDF (NCERT textbook)
   │  PyMuPDF text extraction (+ Tesseract OCR fallback for garbled/scanned pages)
   ▼
Cleaning & chunking (header/footer stripping, ~400-word semantic chunks)
   │  BAAI/bge-small-en-v1.5 embeddings
   ▼
FAISS vector store (MMR retrieval, top_k=4 / fetch_k=12)
   │
   ▼
LangChain pipeline → LLM (Groq llama-3.1-8b-instant, or local Ollama llama3.2:3b)
   │
   ▼
FastAPI (/chat, /generate-quiz, /submit-mcq, /evaluate)
   │
   ▼
React (Vite + Tailwind) frontend
```

| Layer | Choice |
|---|---|
| Backend | FastAPI |
| LLM | Groq (`llama-3.1-8b-instant`) in production, Ollama (`llama3.2:3b`) for local/offline dev |
| Orchestration | LangChain |
| Embeddings | `BAAI/bge-small-en-v1.5` (HuggingFace) — chosen to keep the container under free-tier PaaS RAM limits |
| Vector store | FAISS (local, MMR search) |
| PDF/OCR | PyMuPDF, Tesseract (`pytesseract`) |
| Frontend | React 19, Vite, Tailwind CSS v4 |
| Deployment | Single multi-stage Docker image (frontend build → Python runtime), served as one origin |

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/chat` | `{question}` → `{answer, sources}` |
| POST | `/generate-quiz` | `{question}` → `{quiz, mcqs}` |
| POST | `/submit-mcq` | `{answers: {"1": "A", ...}}` → `{score, details}` |
| POST | `/evaluate` | `{question, answer}` → `{evaluation, weak_topics, suggestions}` |

## Getting started

### Prerequisites
- Python 3.11+
- Node.js 20+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and on `PATH` (only needed to rebuild the index from scanned/garbled PDFs)
- Either a [Groq API key](https://console.groq.com/) **or** [Ollama](https://ollama.com/) running locally with `llama3.2:3b` pulled

### 1. Backend

```bash
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt

cp .env.example .env  # then fill in GROQ_API_KEY, or leave blank to use local Ollama
```

Build the vector index (only needed once, or after adding new source PDFs to `data/raw/`):

```bash
python run_pipeline.py
```

Run the API:

```bash
uvicorn main:app --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server proxies API calls to `http://127.0.0.1:8000`.

### 3. Docker (single-image, production-style)

```bash
docker build -t cbse-smart-assistant .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key cbse-smart-assistant
```

This bakes in the pre-built `faiss_index/` and the compiled frontend, and serves everything from one FastAPI process.

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | No | If set, uses Groq's hosted LLM API. If unset, falls back to local Ollama. |
| `GROQ_MODEL` | No | Defaults to `llama-3.1-8b-instant`. |
| `OLLAMA_MODEL` | No | Defaults to `llama3.2:3b`. |
| `HF_TOKEN` | No | HuggingFace token, if needed for gated embedding model downloads. |

## Project structure

```
app/                  # RAG pipeline: ingestion, chunking, embeddings, retrieval, LLM, quiz/eval logic
main.py               # FastAPI entrypoint & routes
run_pipeline.py        # Rebuilds the FAISS index from data/raw/
frontend/             # React + Vite + Tailwind UI
data/raw/              # Source textbook PDFs
faiss_index/           # Persisted vector index
Dockerfile             # Multi-stage build: frontend → backend runtime
```

## Known limitations

- No automated test suite yet.
- No CI/CD pipeline configured.
- Single subject/class indexed (NCERT Class 10 Science); adding more requires re-running `run_pipeline.py` with new PDFs.

## License

No license specified yet.