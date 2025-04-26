# Insuragen - Reliable Insurance Response Engine built with MultiDomain RAG and Smart Reranking

**AI-Powered Insurance Chatbot with Multi-Domain RAG and Smart Reranking**

---

## 🚀 Project Setup & Running Instructions

Before proceeding, make sure you're on the `dev` branch to access all code and development files:

```bash
git checkout dev
```

### 🐳 Step 1: Local LLM Setup with Docker

To run the chatbot locally using a powerful open-source LLM (like Mistral), follow the steps below:

1. **Install Docker**

   - [Docker Desktop](https://www.docker.com/products/docker-desktop/)

2. **Pull Mistral or any compatible local model**

```bash
docker pull ollama/mistral
```

3. **Run the LLM Server**

```bash
ollama serve
```

Or using Docker directly:

```bash
docker run -d -p 11434:11434 --name ollama ollama/mistral
```

Make sure your LLM is accessible at `http://localhost:11434`.

---

### 💻 Step 2: Starting the Streamlit App

1. **Install Python Dependencies**

```bash
pip install -r requirements.txt
```

2. **Run the Application**

```bash
streamlit run app.py
```

Make sure ports are open if hosted remotely. By default, Streamlit uses port `8501`.

---

## 🧠 About the Project

**InsuraGen** is an advanced domain-aware Retrieval-Augmented Generation (RAG) chatbot tailored for the **Insurance Sector**. It helps customers understand insurance policies across different categories (e.g., Health, Life, Auto, and Home) by answering natural language queries with grounded information from relevant documents.

### ✅ Key Benefits

- Supports **multi-departmental document segregation** (i.e., domain-based chunking).
- Smart **cross-encoder reranking** ensures only top-quality context is used for answering.
- **Modular design** with pluggable LLM, Reranker, Vector DBs (FAISS).
- Live **chat history**, user-friendly **Streamlit UI**, and document preview.
- Future-ready with **API exposure** and **Dockerized LLM support**.

---

## 🔍 What's Advanced: Multi-Domain Reranking

### 🏢 Why Multi-Domain?

Insurance firms operate in silos: Auto, Life, Health, and Home each have dedicated documents. Searching across a flat, mixed chunk space is error-prone and inefficient.

### 🎯 Solution

We create **domain-wise FAISS indices**, each with chunked text and metadata. For a given query:

1. Top-k chunks are fetched from **each domain**.
2. All candidate chunks (`k * num_domains`) are **reranked using a cross-encoder model** (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`).
3. Final top-m reranked chunks are passed to the LLM.

This ensures:

- Semantic relevance
- Domain-diversity
- Robustness to ambiguous queries

### 🤖 Why Reranking?

Sparse retrieval (vector search) can misfire, especially on vague queries. Reranking allows fine-grained relevance scoring based on both the **query** and the **chunk**.

---

## ⚖️ Why This Method Was Chosen

We considered several RAG structures:

### ❌ Traditional RAG

- Vector search retrieves top-k from a single large index.
- Not optimal for siloed data.
- Prone to noisy or misclassified results.

### ⚠️ RAPTOR (Recursive Summarization)

- Graph-based summarization for scalable chunking.
- Better for long, structured documents.
- But complex, hard to maintain for domain-separated corpora.
- Summarization discards valuable specificity needed in insurance queries.

### ✅ Final Chosen Strategy

- **Flat domain-wise indices** (easy to maintain)
- **Cross-encoder reranking** (state-of-the-art relevance)
- **No pre-summarization** (full retention of facts)
- Streamlined for real-world insurance use-cases

---

## 🌐 API-First Design (Planned)

We plan to expose the RAG logic via a REST API using FastAPI:

### Planned Endpoints

- `POST /query`: Ask a question
- `GET /domains`: List document domains
- `POST /upload`: Upload a PDF into a specific domain
- `GET /docs/{domain}`: View chunks

This makes it easily integrable with CRM systems, web portals, and mobile apps.

---

## 🧹 System Architecture

```text
[User]
  |
  | Ask Query
  v
[Streamlit UI] --> [FastAPI (Planned)]
  |
  | QueryController.query(query)
  v
[Vector Search]
  |-> Search domain-1 FAISS index (Top k)
  |-> Search domain-2 FAISS index (Top k)
  |-> ...
  v
[All candidate chunks]
  --> [Reranker (Cross-Encoder)]
        |-> Select top-m reranked chunks
        v
[Prompt Builder]
  --> Stream to LLM
        v
[LLM Response (via Ollama/Mistral)]
  --> UI (streamed display + blinking cursor)
```

---

## 💡 Challenges Faced

### 1. **Choosing Retrieval Structure**

- RAPTOR seemed elegant but unsuitable for multi-domain setups.
- Traditional RAG lacked domain awareness.
- We debated several edge-weighted retrieval options.
- Eventually chose flat-per-domain indices with reranking for flexibility.

### 2. **LLM Streaming UX**

- Streamlit does not stream like a websocket.
- We added interim messages (e.g., "Thinking...") to fix perceived lag.

### 3. **Embedding + Metadata Storage**

- Balancing pickle file storage for chunks with scalable FAISS usage.
- Designed a modular class-based `DomainVectorStore`.

### 4. **Deployment Planning**

- Built for local testing with Docker-based LLMs.
- Future: cloud LLM, serverless vector DBs (like Pinecone), and FastAPI hosting.

---

## 🛠️ Directory Structure (Simplified)

```
core/
  services/
    reranking/
    vector/
    query_controller.py
  ui/
    views/
    session_state.py
app.py
requirements.txt
Dockerfile
```

---

## 🧪 Further Work

- ✅ Convert internal logic into APIs using FastAPI
- ✅ Add support for uploading documents from UI
- 🟡 PDF OCR support for scanned forms
- 🟡 Add document tagging and priority scoring
- 🟢 Add user feedback rating to improve reranker
- 🔄 Sync vector store with cloud
- 📊 Add analytics and query logging

---

## 📩 Support & Feedback

If a query is unanswered due to lack of document coverage, the assistant guides users to email:

```
supportEmail@help.com
```

This ensures fallback to human agents.

---

## 🙌 Contributing

- Fork and clone this repo.
- Setup virtual env, install dependencies.
- Submit PRs via `dev` branch.

### 📂 Branching Strategy

- **`main` branch** contains the latest stable **README and documentation only**.
- All active development, including code, features, and bugfixes, happens on the **`dev` branch**.
- If you want to **view or contribute to the code**, please switch to the `dev` branch:

```bash
git checkout dev
```

We keep the `main` branch clean to ensure smooth previewing for hackathon judges or stakeholders.

---

## 📜 License

MIT License — Feel free to adapt and extend this project.

---

Built with ❤️ by Team InsuraGen for the TCS Hackathon 2025.
