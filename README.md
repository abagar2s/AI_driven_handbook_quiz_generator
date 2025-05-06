# 📘 Handbook & Quiz Generator

This is a full-stack AI-powered application that allows users to upload documents (such as resumes or training content), from which it generates a structured **training handbook** and **multiple-choice quiz questions** using LLaMA 2. The system is built with **FastAPI (Python)** for the backend and **React (TypeScript)** for the frontend.

## 🧩 Features

- 📄 Upload one or more PDF/text documents.
- 🧠 LLaMA 2-based summarization and question generation.
- 📘 Outputs a clean, structured training handbook.
- ❓ Generates 5 multiple-choice questions with support for **multiple correct answers**.
- 🌐 React-based frontend with drag-and-drop UX.
- ✅ Supports semantic chunking and clustering for optimal processing.

## 🏗️ Tech Stack

- **Backend**: FastAPI, Python, llama.cpp (via `llama_cpp`)
- **Frontend**: React + TypeScript
- **Model**: `llama-2-7b-chat.Q4_K_M.gguf` (local inference)

## 📁 Folder Structure

```
app/
├── main.py              # FastAPI app entrypoint
├── upload.py            # API route: handles file upload, handbook creation, and quiz generation
├── utils/
│   ├── extract.py       # Text extraction from uploaded files
│   ├── clean.py         # Cleaning text (remove metadata, whitespace, etc.)
│   ├── chunker.py       # Chunk and cluster text semantically
│   ├── clusterer.py     # Clustering (agglomerative) logic
│   ├── embedder.py      # Text embeddings for semantic operations
├── llama_runner.py      # Run LLaMA chat completions locally
```

## 🚀 Getting Started

### 1. Backend Setup

#### ✅ Prerequisites

- Python 3.10+
- Install llama.cpp with Python bindings

```bash
pip install -r requirements.txt
```

#### ▶️ Run the backend

```bash
uvicorn app.main:app --reload
```

> Make sure the model file `llama-2-7b-chat.Q4_K_M.gguf` is placed in `./app/models/`.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

> The frontend communicates with `localhost:8000`.

## 📦 API: `/upload`

**Method**: `POST`  
**Params**:

- `files`: list of PDF or text files
- `prompt`: user prompt (optional)

**Returns**:
```json
{
  "handbuch": "...",
  "quiz": [
    {
      "question": "...",
      "answers": ["...", "...", "...", "..."],
      "right_answers": [1, 2]
    }
  ]
}
```

## 🧠 LLaMA Prompting

Prompt chaining is used in these stages:

1. **Summarize** raw document content per semantic chunk.
2. **Format** those summaries into handbook sections.
3. **Generate quiz**: multiple-choice questions using clean JSON schema.

## 🐞 Troubleshooting

- 🟥 **Not getting quiz questions?**  
  Ensure at least 3–5 rich content chunks are extractable and the model responses are parsable JSON.
  
- 📄 **Empty handbook?**  
  Check that the uploaded file isn’t an image-based (non-OCR) PDF.

## 📜 License

MIT