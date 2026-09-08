# Advanced RAG System

An Advanced Retrieval Augmented Generation (RAG) system built to answer questions over PDF documents using hybrid retrieval, query rewriting, and cross-encoder re-ranking.

This project implements a multi-stage retrieval pipeline designed to improve answer quality, reduce hallucination, and provide answers grounded in retrieved document context.

---

# Overview

Large Language Models (LLMs) have strong reasoning capabilities but they have limitations:

- Knowledge is limited to training data
- They may hallucinate facts
- They cannot access private documents directly

Retrieval Augmented Generation (RAG) solves these problems by retrieving relevant information from external documents and providing that context to the LLM before generating an answer.

This project implements an advanced RAG architecture with multiple retrieval improvements:

- Semantic vector search
- Keyword-based retrieval
- Hybrid retrieval
- Query rewriting
- Multi-query expansion
- Cross Encoder re-ranking
- Context management
- Retrieval evaluation

---

# Architecture

## Complete Pipeline

                     PDF Document
                          |
                          v
                 Document Loader
                          |
                          v
                      Chunking
                          |
                          v
                     Embeddings
                          |
                          v
                     ChromaDB

User Question
|
v
Query Rewriter
|
v
Multi Query Generator
|
v
Hybrid Retriever
|
|
+----------------+
| |
v v
Vector Search BM25 Search
| |
+----------------+
|
v
Combined Ranking
|
v
Cross Encoder Re-ranking
|
v
Context Manager
|
v
LLM Generation
|
v
Answer + Sources


---

# Features

## Document Processing

- PDF document loading
- Text chunking
- Metadata preservation
- Embedding generation


## Retrieval System

### Vector Search

Uses semantic similarity search to find documents based on meaning rather than exact keywords.

### BM25 Search

Uses keyword-based retrieval to find documents containing important terms.

### Hybrid Retrieval

Combines both approaches:


Final Score = 0.7 * Semantic Score + 0.3 * BM25 Score


This improves retrieval quality by combining semantic understanding with exact keyword matching.

---

## Query Enhancement

### Query Rewriting

Transforms user questions into improved search queries.

Example:


User:
"What problems does AI have?"

Rewrite:
"What are the limitations and challenges of artificial intelligence?"


---

### Multi Query Retrieval

Generates multiple search variations to increase retrieval coverage.

Example:


Original query:
"What is machine learning?"

Generated queries:

Explain machine learning concepts
Machine learning definition
How machine learning algorithms work

---

## Re-ranking

The system uses a Cross Encoder model after initial retrieval.

Pipeline:


Hybrid Retriever

   |
   v

Top 10 candidate chunks

   |
   v

Cross Encoder

   |
   v

Top 5 relevant chunks


Unlike embedding models that compare query and document separately, Cross Encoders evaluate:


(query, document)


together, providing more accurate relevance scoring.

Model:


cross-encoder/ms-marco-MiniLM-L-6-v2


---

# Tech Stack

## Core

- Python
- ChromaDB
- Sentence Transformers
- BM25
- Pytest


## LLM

Supports external LLM APIs for answer generation.

Configuration is managed through environment variables.

---

# Project Structure


week3/

├── document_loader/
│ ├── pdf_loader.py
│ └── splitter/
│ └── chunker.py
│
├── embeddings/
│ └── embedder.py
│
├── vector_store/
│ └── chroma_db.py
│
├── retrieval/
│ ├── vector_retriever.py
│ ├── bm25_retriever.py
│ ├── hybrid_retriever.py
│ └── reranker.py
│
├── query/
│ ├── query_rewriter.py
│ └── multi_query.py
│
├── context/
│ └── context_manager.py
│
├── generation/
│ └── answer_generator.py
│
├── evaluation/
│ ├── dataset.py
│ ├── metrics.py
│ └── evaluate.py
│
├── tests/
│
├── rag_pipeline.py
├── requirements.txt
└── README.md


---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd week3
Create Virtual Environment
python -m venv .venv

Activate:

macOS / Linux
source .venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Environment Configuration

Create a .env file:

OPENROUTER_API_KEY=your_api_key

CHAT_MODEL=your_chat_model

EMBED_MODEL=your_embedding_model
Running the Project
Ask Questions

Run the RAG pipeline:

python rag_pipeline.py

The system will:

Rewrite the query
Generate multiple queries
Retrieve documents using hybrid search
Re-rank retrieved chunks
Generate an answer using the LLM
Return sources
Testing

Run all tests:

pytest

Tests cover:

Embedding functionality
Retrieval
Hybrid search
Metadata filtering
Query rewriting
Multi-query retrieval
Re-ranking
Evaluation

The project includes an evaluation pipeline to measure retrieval quality.

Evaluation checks:

Retrieved context relevance
Generated answer correctness
Retrieval precision

Run evaluation:

python -m evaluation.evaluate
Example Workflow

User:

What are the limitations of artificial intelligence?

System:

1. Rewrite query

2. Generate search variations

3. Hybrid retrieval

4. Retrieve candidate chunks

5. Cross Encoder re-ranking

6. Generate final answer

Output:

Answer:
AI systems have limitations including
data dependency, bias, and lack of general intelligence.

Sources:
- Document page references
- Retrieved chunks
Design Decisions
Why Hybrid Search?

Vector search provides semantic understanding, while BM25 provides strong keyword matching.

Combining both improves retrieval robustness.

Why Re-ranking?

Initial retrieval focuses on speed.

Cross Encoder re-ranking focuses on accuracy.

This two-stage retrieval strategy provides a balance between:

Retrieval speed
Answer relevance
Future Improvements

Possible improvements:

Add RAGAS evaluation
Add LLM-as-a-Judge evaluation
Add conversational memory
Add web search tools
Add API deployment with FastAPI
Add streaming responses
Add document management system
Learning Outcomes

Through this project, the following RAG concepts were implemented:

Document ingestion
Chunking strategies
Embedding-based retrieval
Vector databases
Keyword retrieval
Hybrid search
Query rewriting
Multi-query retrieval
Cross Encoder re-ranking
RAG evaluation
License

This project is for educational and research purposes.