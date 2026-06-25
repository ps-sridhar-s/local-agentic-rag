
# 🚀 Local Agentic RAG Chatbot

An enterprise-grade **Agentic Retrieval-Augmented Generation (RAG)** system built using **LangGraph, LangChain, FastAPI, FAISS, and Ollama**.

The system ingests documents, performs intelligent chunking, generates embeddings, stores them in a vector database, and enables users to interact with their knowledge base through a modern conversational interface.

---

# ✨ Features

* 📄 Multi-document ingestion (PDF support)
* 🧠 Agentic RAG pipeline using LangGraph
* 🔍 Semantic similarity retrieval using FAISS
* 💬 Conversational AI with local LLMs via Ollama
* 🛡️ Basic Guardrails for unsafe content detection
* 🧩 Multiple chunking strategies
* ⚡ FastAPI backend APIs
* 🎨 Responsive HTML/CSS/JavaScript frontend
* 🧪 Unit testing using Pytest
* 📜 Detailed logging support
* 🔄 Intent detection (Chit-chat vs Knowledge Retrieval)
* 🏠 Fully local deployment (No external API dependency)

---

# 🏗️ Architecture

```text
                        +----------------+
                        | User Interface |
                        | HTML/CSS/JS    |
                        +--------+-------+
                                 |
                                 v
                        +----------------+
                        |    FastAPI     |
                        |    Backend     |
                        +--------+-------+
                                 |
                                 v
                     +---------------------+
                     | LangGraph Workflow  |
                     +---------------------+
                                 |
          +----------------------+------------------+
          |                                         |
          v                                         v
+---------------------+                +----------------------+
| Chit Chat Agent     |                | Retrieval Agent      |
+---------------------+                +----------+-----------+
                                                  |
                                                  v
                                    +-------------------------+
                                    | FAISS Vector Database   |
                                    +-------------------------+
                                                  |
                                                  v
                                    +-------------------------+
                                    | Ollama Embedding Model  |
                                    +-------------------------+
                                                  |
                                                  v
                                    +-------------------------+
                                    | Local LLM (Ollama)      |
                                    +-------------------------+
```

---

# 🛠️ Tech Stack

## Backend

* Python 3.11+
* FastAPI
* Uvicorn

## AI / GenAI

* LangChain
* LangGraph
* Ollama
* Retrieval-Augmented Generation (RAG)

## Vector Database

* FAISS

## Embedding Models

* `mxbai-embed-large`

## Large Language Models

* Llama 3
* Gemma
* Mistral
* Any Ollama-supported LLM

## Frontend

* HTML5
* CSS3
* JavaScript

## Testing

* Pytest

## Logging

* Python Logging Module

---

# 📂 Project Structure

```text
Local_Agentic_Rag
│
├── chunking/                  # Chunking strategies
├── data_source/               # Source documents
├── data_warehouse/            # Vector database storage
├── document_loader/           # Document loaders
├── embedding/                 # Embedding generation
├── generation/                # LLM response generation
├── models/                    # Chat & embedding models
├── pipeline/                  # LangGraph workflows
├── similarity_retrieval/      # Retrieval strategies
├── static/                    # Frontend files
├── unit_testing/              # Unit tests
│
├── app.py                     # FastAPI entry point
├── requirements.txt           # Dependencies
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/Local_Agentic_Rag.git

cd Local_Agentic_Rag
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Install Ollama

Download and install Ollama:

https://ollama.com

Pull required models:

```bash
ollama pull llama3

ollama pull mxbai-embed-large
```

---

# 📥 Document Ingestion

Place PDF documents inside:

```text
data_source/
```

Run indexing pipeline:

```bash
python -m pipeline.orchestrator
```

This will:

1. Load documents
2. Clean documents
3. Chunk documents
4. Generate embeddings
5. Store vectors in FAISS

---

# 🚀 Running the Application

Start FastAPI server:

```bash
uvicorn app:app --reload --port 8111
```

Open browser:

```text
http://127.0.0.1:8111
```

---

# 🔄 LangGraph Workflow

```text
START
   |
   v
User Query
   |
   v
Guardrails
   |
   +---- Unsafe ----> Reject Response
   |
   v
Intent Detection
   |
   +---- Chit Chat ----> Chat Agent
   |
   +---- RAG ----------> Retriever
                                  |
                                  v
                             FAISS Search
                                  |
                                  v
                             RAG Agent
                                  |
                                  v
                                 END
```

---

# 🧪 Running Unit Tests

Execute all tests:

```bash
pytest
```

Run specific test:

```bash
pytest unit_testing/test_vector_search.py
```

---

# 📊 Retrieval Techniques Supported

* Similarity Search
* Hybrid Search
* Full Text Search
* Top-K Retrieval

---

# 🔒 Guardrails

The system includes:

* Unsafe query detection
* Restricted keyword filtering
* Intent classification

---

# 📈 Future Enhancements

* Multi-agent orchestration
* Conversational memory
* Human-in-the-loop workflows
* Re-ranking
* Hybrid retrieval with BM25 + Vector Search
* Evaluation framework (RAGAS)
* Streaming responses
* Authentication & Authorization
* Docker deployment
* Kubernetes deployment

---

# 👨‍💻 Author

**Sridhar S**

AI Engineer | Agentic AI | GenAI | RAG | LangGraph | LangChain


