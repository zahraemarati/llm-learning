# AI Research Assistant

An AI-powered research assistant built with LangChain, RAG, hybrid retrieval, reranking, tools, agents, memory, and LLM-based report generation.

The project can retrieve information from indexed PDF documents, answer research questions with source references, summarize retrieved information, and generate structured research reports.

---

## Problem

Large research documents are difficult to search manually.

A user may want to ask questions such as:

```text
What are the major development trends of intelligent technologies?
```

Instead of reading the entire document, the system retrieves the most relevant sections, reranks them, generates an answer based only on the retrieved context, and creates a structured research report.

---

## Architecture

```text
                        User
                          |
                          v
                     AI Assistant
                          |
              -------------------------
              |           |           |
              v           v           v
          Web Search    RAG Tool   Calculator
                          |
                          v
                  Query Rewriting
                          |
                          v
                  Multi Query Generation
                          |
                          v
                   Hybrid Retrieval
                    /           \
                   v             v
             Vector Search    BM25 Search
                    \           /
                     v         v
                      Reranker
                          |
                          v
                     Context
                          |
                          v
                    LLM Answer
                          |
                          v
                    Summarizer
                          |
                          v
                 Report Generator
                          |
                          v
                Markdown Research Report
```

---

## Features

- Retrieval-Augmented Generation (RAG)
- Semantic vector search
- BM25 keyword search
- Hybrid retrieval
- Document reranking
- Query rewriting
- Multi-query generation
- PDF document retrieval
- Source-aware answers
- LangChain retrievers
- LangChain chains
- Prompt templates
- Conversation memory
- Tool calling
- AI agent with multiple tools
- Web search tool
- Calculator tool
- Research report generation
- Automated tests with pytest

---

## Technologies

- Python
- LangChain
- OpenAI-compatible APIs
- OpenRouter
- ChromaDB
- BM25
- Hugging Face models
- PyPDF
- DDGS
- Pydantic
- Pytest

---

## Project Structure

```text
week4/
│
├── agents/
│   ├── research_agent.py
│   └── research_assistant.py
│
├── chains/
│   ├── conversational_chain.py
│   ├── qa_chain.py
│   ├── rag_chain.py
│   ├── report_chain.py
│   ├── simple_chain.py
│   └── summarizer_chain.py
│
├── context/
│   └── context_manager.py
│
├── document_loader/
│
├── embeddings/
│   └── embedder.py
│
├── generation/
│   └── answer_generator.py
│
├── memory/
│   ├── buffer_memory.py
│   └── summary_memory.py
│
├── prompts/
│   ├── conversation_prompt.py
│   ├── rag_prompt.py
│   ├── report_prompt.py
│   └── research_prompt.py
│
├── query/
│   ├── multi_query.py
│   └── query_rewriter.py
│
├── retrieval/
│   ├── bm25_retriever.py
│   ├── hybrid_retriever.py
│   ├── reranker.py
│   └── vector_retriever.py
│
├── retrievers/
│   ├── hybrid_retriever.py
│   └── vector_retriever.py
│
├── tools/
│   ├── calculator.py
│   ├── pdf_reader.py
│   ├── rag_tool.py
│   └── web_search.py
│
├── tests/
│
├── report/
│   └── research_report.md
│
├── scripts/
│   └── generate_report.py
│
├── config.py
├── llm_client.py
├── rag_pipeline.py
├── main.py
└── requirements.txt
```

---

## RAG Pipeline

The RAG pipeline follows these steps:

```text
Question
   |
   v
Query Rewrite
   |
   v
Multi Query Generation
   |
   v
Hybrid Retrieval
   |
   +------ Vector Search
   |
   +------ BM25 Search
   |
   v
Reranking
   |
   v
Context Selection
   |
   v
LLM Generation
   |
   v
Answer + Sources
```

The hybrid retrieval approach combines semantic similarity with keyword-based search.

The reranker then selects the most relevant chunks before they are sent to the language model.

---

## Agent Tools

The research agent can work with multiple tools.

### RAG Search

Searches indexed research documents and returns:

```python
{
    "answer": "...",
    "sources": [...]
}
```

### Web Search

Searches external web content using DDGS.

### Calculator

Performs mathematical calculations when the user asks a calculation question.

Example:

```text
User:
Calculate 25 * 25

Agent:
Uses calculator tool

Answer:
625
```

---

## Research Report Generation

The research assistant converts retrieved information into a structured Markdown report.

The generated report contains:

```text
# Title

## Abstract

## Main Findings

## Comparison

## Conclusion

## Sources
```

Example output:

```markdown
# Research Report on Intelligent Technologies Development Trends

## Abstract
This report analyzes major development trends of intelligent technologies...

## Main Findings
- Intelligent robots
- AR/VR
- Artificial Intelligence
- Big Data

## Sources
- Huawei Global Industry Outlook Report, pages 33, 43, 52, 53
```

Reports can also be written to:

```text
report/research_report.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/zahraemarati/llm-learning.git
```

Move into the project:

```bash
cd llm-learning/week4
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_openrouter_api_key

CHAT_MODEL=openai/gpt-4o-mini

EMBED_MODEL=nvidia/nemotron-3-embed-1b:free
```

Do not commit `.env` to GitHub.

An optional Hugging Face token can also be configured to avoid unauthenticated Hub warnings.

---

## Run the Application

Run the interactive demo:

```bash
python main.py
```

Example:

```text
AI Research Assistant

Enter your research question:

> What are the major development trends of intelligent technologies?

Generating research report...
```

The assistant retrieves relevant information and generates a structured research report.

---

## Generate a Report

You can also run:

```bash
python -m scripts.generate_report
```

The generated Markdown report is stored in:

```text
report/research_report.md
```

---

## Testing

Run the complete test suite:

```bash
python -m pytest -v
```

The test suite covers:

- Embeddings
- Vector retrieval
- Hybrid retrieval
- BM25 retrieval
- Metadata filtering
- Query rewriting
- Multi-query generation
- Reranking
- RAG pipeline
- LangChain retrievers
- Chains
- Agent tool usage

Current test status:

```text
All tests passing
```

---

## Example End-to-End Flow

```text
User Question
      |
      v
Query Rewrite
      |
      v
Multi Query
      |
      v
Hybrid Retriever
      |
      v
Reranker
      |
      v
Relevant Context
      |
      v
LLM Answer
      |
      v
Summarizer
      |
      v
Report Generator
      |
      v
Research Report + Sources
```

---

## Key Concepts Demonstrated

This project demonstrates practical implementations of:

- Large Language Models
- Retrieval-Augmented Generation
- Semantic Search
- Hybrid Search
- Prompt Engineering
- LangChain LCEL
- Retrievers
- Tools
- Agents
- Tool Calling
- Conversation Memory
- Reranking
- Research Report Generation

---

## Future Improvements

Possible future improvements include:

- Automatically routing research questions between web search and internal RAG
- Adding structured source citations
- Adding asynchronous tool execution
- Adding persistent conversational memory
- Adding a web-based user interface
- Adding RAG evaluation metrics
- Adding tracing and observability
- Replacing deprecated LangChain components with their newer equivalents

---

## Author

Built as part of an LLM engineering learning project focused on building production-style RAG and agentic AI applications.