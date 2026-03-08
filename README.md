# 📘 Hellobooks AI Accounting Assistant

An AI-powered accounting assistant built using a **Retrieval-Augmented Generation (RAG)** architecture. This tool helps users query accounting documents like bookkeeping records, invoices, and financial statements using natural language.

---

## 🚀 Overview

This prototype leverages RAG to provide accurate, context-aware answers. Instead of relying solely on an LLM's general knowledge, it retrieves relevant data from your specific accounting documents (TXT/Markdown) to generate precise responses.

## ✨ Features

- **Document Ingestion**: Upload accounting documents in `.txt` or `.md` format.
- **Smart Chunking**: Automatic text splitting for better context retrieval.
- **Vector Search**: Uses **ChromaDB** and **SentenceTransformers** for high-accuracy similarity search.
- **Groq AI Integration**: Lightning-fast responses using the Groq LLM API.
- **Streamlit UI**: A clean and simple chat interface for interacting with the assistant.
- **Dockerized**: Easy deployment using Docker containers.

---

## 🏗️ Project Architecture

The system follows a standard RAG workflow:
1. **Ingestion**: Documents are parsed and split into chunks.
2. **Embedding**: Each chunk is converted into a vector using `SentenceTransformers`.
3. **Storage**: Vectors are stored in **ChromaDB**.
4. **Retrieval**: When a user asks a question, the system finds the most relevant chunks.
5. **Generation**: The retrieved chunks are sent to the **Groq LLM** as context to produce the final answer.

---

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Streamlit
- **Vector Database**: ChromaDB
- **Embeddings**: SentenceTransformers
- **LLM**: Groq API
- **DevOps**: Docker

---

## 📂 Project Structure

```text
hellobooks-rag-assistant/
├── main.py              # FastAPI Entry point
├── ui.py                # Streamlit Interface
├── .env                 # Environment variables
├── Dockerfile           # Docker configuration
├── requirements.txt     # Dependencies
├── README.md            # Documentation
├── knowledge_base/      # Sample accounting docs
│   ├── bookkeeping.md
│   ├── invoices.md
│   ├── profit_loss.md
│   └── ...
├── backend/             # Core logic
│   ├── database.py
│   ├── groq_client.py
│   ├── routes.py
|   ├── utils/               # Helper scripts
|   ├── chunking.py
|   ├── embeddings.py
|   └── vectorstore.py
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```Bash
git clone [[https://github.com/mdpatel007/hellobooks-rag-assistant.git](https://github.com/mdpatel007/hellobooks-rag-assistant.git)](https://github.com/mdpatel007/AI-Accounting-Chatbot.git)

cd hellobooks-rag-assistant 
```

### 2. Install Dependencies
```Bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a .env file in the root directory and add your credentials:

```Bash
GROQ_API_KEY=your_groq_api_key
CHROMA_DIR=chroma_db
MONGO_URI=your_mongo_connection_string
MONGO_DB=chatdb
```

### 4. Run the Application
Start Backend (FastAPI):

```Bash
uvicorn main:app --reload
```

Start Frontend (Streamlit):

```Bash
streamlit run ui.py
```

---

## 🐳 Docker Support
To run the application using Docker:

### 1. Build the Image:

```Bash
docker build -t hellobooks-ai .
```

### 2. Run the Container:

```Bash
docker run -p 8000:8000 hellobooks-ai
```

---

## ❓ Example Questions

- "What is the difference between revenue and profit?"
- "What information should be included in a standard invoice?"
- "Explain the importance of a Cash Flow statement."

## 👤 Author
Mihir Dudhat
