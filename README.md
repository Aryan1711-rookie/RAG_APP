# Smriti.AI 🧠

Smriti.AI is a Retrieval-Augmented Generation (RAG) web application built with Flask, ChromaDB, Sentence Transformers, and Groq LLMs. It allows users to upload documents, build a searchable knowledge base, and chat with their documents using semantic search and large language models.

---

## Features

* Upload PDF documents
* Automatic document chunking
* Semantic embeddings using BAAI/bge-base-en-v1.5
* ChromaDB vector database integration
* Retrieval-Augmented Generation (RAG)
* Groq-powered responses
* Modern chat interface
* Persistent local knowledge base
* Metadata tracking (source file, page number, file type)
* Duplicate document detection using file hashing
* Extensible loader architecture for future support of TXT, HTML, DOCX, CSV, and SQL sources

---

## Architecture

```text
User Upload
    ↓
Document Loader
    ↓
Chunking
    ↓
Embedding Generation
    ↓
ChromaDB Vector Store
    ↓
Retriever
    ↓
Groq LLM
    ↓
Response Generation
```

---

## Tech Stack

### Backend

* Flask
* ChromaDB
* Sentence Transformers
* Groq API
* LangChain

### Frontend

* HTML
* CSS
* JavaScript

### Embedding Model

* BAAI/bge-base-en-v1.5

### LLM

* Llama 3.3 70B Versatile (Groq)

---

## Project Structure

```text
RAG_WEB_APP/
│
├── app.py
│
├── loaders/
│   ├── base_loader.py
│   ├── pdf_loader.py
│   └── __init__.py
│
├── rag/
│   ├── ingestion.py
│   ├── retriever.py
│   └── generator.py
│
├── embeddings/
│   └── embedding_manager.py
│
├── vector_db/
│   └── vector_store.py
│
├── llm/
│   └── groq_client.py
│
├── templates/
│   ├── index.html
│   └── chat.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── chat.js
│
├── data/
│   ├── pdf/
│   └── vector_store/
│
└── tests/
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Aryan1711-rookie/RAG_APP.git
cd RAG_WEB_APP
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Running the Application

```bash
python app.py
```

Application will be available at:

```text
http://127.0.0.1:5000
```

---

## Uploading Documents

1. Open homepage
2. Upload a PDF document
3. The document is:

   * Loaded
   * Chunked
   * Embedded
   * Stored in ChromaDB

The document becomes immediately searchable.

---

## Knowledge Base

All uploaded documents are stored inside a shared knowledge base.

Example:

```text
Knowledge Base
│
├── Transformer.pdf
├── ResearchNotes.pdf
├── Hyperspectral.pdf
└── DefenceNotes.pdf
```

Queries search across every uploaded document automatically.

---

## Example Questions

```text
How many attention heads are used in the Transformer?

Explain self-attention.

What is hyperspectral imaging?

Summarize the uploaded paper.
```

---

## Metadata Stored

Each chunk stores:

```json
{
  "source_file": "Attention is all you need.pdf",
  "file_type": "pdf",
  "page": 4,
  "file_hash": "...",
  "doc_index": 17
}
```

This enables source attribution and document management.

---

## Current Limitations

* PDF loader only
* Local ChromaDB storage
* Single-user deployment
* No authentication
* No chat history persistence

---

## Planned Features

* TXT Loader
* HTML Loader
* DOCX Loader
* CSV Loader
* SQL Loader
* Source citations in chat
* Streaming responses
* Multi-file upload
* User authentication
* Cloud storage integration
* Supabase pgvector support
* Cloud deployment

---

## Future Deployment Architecture

```text
User
 ↓
Flask
 ↓
Cloudflare R2
 ↓
Embeddings
 ↓
Supabase pgvector
 ↓
Retriever
 ↓
Groq LLM
 ↓
Response
```

---


