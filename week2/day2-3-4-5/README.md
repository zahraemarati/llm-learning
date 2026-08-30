# PDF Chat Assistant

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![LangChain](https://img.shields.io/badge/LangChain-RAG-orange)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple)

A Retrieval-Augmented Generation (RAG) based application that allows users to interact with PDF documents using natural language.

The system processes PDF files, converts document content into semantic embeddings, stores them in a vector database, retrieves relevant information, and generates grounded answers using an LLM.

---

# Project Overview

PDF Chat Assistant is an AI-powered document question-answering system built using the RAG (Retrieval-Augmented Generation) architecture.

Instead of sending the entire document to a language model, the application:

1. Loads PDF documents
2. Splits text into meaningful chunks
3. Creates vector embeddings
4. Stores embeddings in a vector database
5. Retrieves relevant sections based on user questions
6. Generates answers using retrieved context only

The goal is to build a reliable AI assistant that can answer questions from private documents while providing source references.

---

# Architecture

```
                 PDF Document

                       |
                       v

                PDF Loader

                       |
                       v

                  Chunking

                       |
                       v

              Embedding Model

                       |
                       v

                ChromaDB

              Vector Database

                       |
                       v

                Retriever

                       |
                       v

             Context Manager

                       |
                       v

                    LLM

                       |
                       v

               Final Answer
```

---

# Features

## Document Processing

- PDF document loading
- Automatic text extraction
- Intelligent text chunking
- Semantic embedding generation

## Retrieval System

- Vector similarity search
- ChromaDB based vector storage
- Context-aware retrieval
- Relevant document source tracking

## Question Answering

- Natural language questions
- RAG-based answer generation
- Answers grounded only on retrieved context
- Source citation support

## API

- FastAPI REST API
- Request validation with Pydantic
- Error handling
- API documentation with Swagger UI

## User Interface

- Simple Streamlit frontend
- Interactive document question answering

---

# Tech Stack

## Programming Language

- Python

## Backend

- FastAPI
- Pydantic

## AI / LLM

- OpenAI Compatible API
- OpenRouter
- Embedding Models

## RAG Components

- LangChain
- ChromaDB
- Vector Search
- Semantic Retrieval

## Frontend

- Streamlit

## Testing

- Pytest

---

# Project Structure

```
pdf-chat-assistant/

├── backend/
│   └── API implementation
│
├── document_loader/
│   ├── PDF loader
│   └── text chunking
│
├── embeddings/
│   └── embedding generation
│
├── retrieval/
│   └── semantic search
│
├── vector_store/
│   └── vector database interface
│
├── context/
│   └── context management
│
├── generation/
│   └── answer generation
│
├── frontend/
│   └── Streamlit application
│
├── tests/
│   └── unit tests
│
├── rag_pipeline.py
├── config.py
├── llm_client.py
└── requirements.txt
```

---

# Installation

Clone the repository:

```bash
git clone <repository-url>

cd pdf-chat-assistant
```

Create virtual environment:

```bash
python -m venv venv

source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment variables:

```bash
cp .env.example .env
```

Add your API configuration inside `.env`.

---

# Running the Application

## Start Backend

```bash
uvicorn backend.main:app --reload
```

API documentation:

```
http://127.0.0.1:8000/docs
```

---

## Start Frontend

```bash
streamlit run frontend/app.py
```

---

# Example

## Question

```
What is Artificial Intelligence?
```

## Answer

```
Artificial Intelligence is a field of computer science
focused on creating systems capable of performing tasks
that normally require human intelligence.

Sources:
- Page 13
- Page 16
- Page 17
```

---

# Screenshots

(Add application screenshots here)

---

# Demo Video

(Add 1 minute project demonstration video here)

---

# Future Improvements

Planned improvements:

- Hybrid Search
- Re-ranking models
- Query rewriting
- RAG evaluation pipeline
- Enterprise document management
- Multi-user authentication

---

# Author

Built as an AI Engineering learning project focused on Retrieval-Augmented Generation systems.
