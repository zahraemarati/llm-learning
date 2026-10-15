# Multi-Agent Research Assistant

A modular LLM application that combines tool-using agents, Retrieval-Augmented Generation, conversation memory, planning, and a multi-agent workflow.

The project was built incrementally to explore how production-style LLM systems can move from a single tool-using agent to a structured multi-agent pipeline.

## Features

- Tool-using LLM agents
- Calculator tool
- PDF reader tool
- Web search tool
- Retrieval-Augmented Generation
- Vector search with ChromaDB
- BM25 keyword retrieval
- Hybrid retrieval
- Cross-encoder reranking
- Conversation buffer memory
- Summary memory
- Context management
- Planning and task decomposition
- Reflection and execution loop
- Agent base architecture
- Tool injection
- Role-based agents
- Agent delegation
- Shared workflow state
- Multi-agent communication
- Error handling
- Unit and regression tests

## Architecture

```text
                         User
                          |
                          v
                    Manager Agent
                          |
                          v
                   Research Agent
                          |
                          v
                     Writer Agent
                          |
                          v
                    Reviewer Agent
                          |
                          v
                  Writer Revision
                          |
                          v
                    Final Answer
```

The research layer can use external tools and the RAG pipeline:

```text
Research Agent
      |
      v
    Tools
      |
      +-------------------+
      |         |         |
      v         v         v
 rag_search  web_search  pdf_reader
      |
      v
 Hybrid Retrieval
      |
      +-------------------+
      |                   |
      v                   v
Vector Search           BM25
      |                   |
      +---------+---------+
                |
                v
             Reranker
                |
                v
             Context
```

## Multi-Agent Workflow

A request such as:

```text
Write a report about paper.pdf
```

is processed through the following workflow:

```text
User Task
   |
   v
Manager
   |
   v
Researcher
   |
   | research_notes
   v
Writer
   |
   | draft
   v
Reviewer
   |
   | review feedback
   v
Writer
   |
   | final_answer
   v
Final Response
```

Each stage writes its result into a shared `WorkflowState`.

## Workflow State

The multi-agent pipeline tracks:

```text
task
research_notes
draft
review
final_answer
current_stage
completed_stages
errors
success
```

This makes the workflow observable and allows the manager to stop execution safely when a stage fails.

## Project Structure

```text
.
├── agents/
│   ├── base_agent.py
│   ├── assistant_agent.py
│   ├── research_agent.py
│   ├── researcher.py
│   ├── writer.py
│   ├── reviewer.py
│   ├── manager.py
│   ├── manager_agent.py
│   ├── planner.py
│   ├── executor.py
│   ├── planning_agent.py
│   ├── prompts.py
│   └── workflow_state.py
│
├── context/
│   ├── context_builder.py
│   └── context_manager.py
│
├── memory/
│   ├── buffer_memory.py
│   └── summary_memory.py
│
├── tools/
│   ├── calculator.py
│   ├── pdf_reader.py
│   ├── web_search.py
│   └── rag_tool.py
│
├── retrieval/
│   ├── hybrid_retriever.py
│   └── reranker.py
│
├── ingestion/
│   └── pdf_ingestor.py
│
├── tests/
│   ├── test_agent_tools.py
│   ├── test_memory.py
│   ├── test_multi_agent.py
│   └── ...
│
├── config.py
├── llm_client.py
├── pyproject.toml
└── README.md
```

## Agent Roles

### Manager

The manager coordinates the workflow and controls execution order.

Responsibilities:

- Start the workflow
- Delegate tasks
- Track workflow state
- Stop execution on failure
- Return the final answer

### Researcher

The researcher gathers information required for the task.

Available capabilities include:

- RAG search
- Web search
- Direct PDF reading

The researcher returns research notes rather than a final report.

### Writer

The writer converts research notes into a structured draft.

It is also responsible for revising the draft after reviewer feedback.

### Reviewer

The reviewer evaluates the draft against:

- Original task
- Research notes
- Correctness
- Relevance
- Completeness
- Structure
- Clarity
- Unsupported claims

The review is returned to the writer for revision.

## RAG Pipeline

The RAG system combines semantic and lexical retrieval.

```text
Query
 |
 +----------------+
 |                |
 v                v
Vector Search    BM25
 |                |
 +-------+--------+
         |
         v
 Reciprocal Rank Fusion
         |
         v
 Cross-Encoder Reranking
         |
         v
 Context Builder
         |
         v
 LLM / Agent
```

Indexed PDF documents are stored in ChromaDB.

## Memory

The project contains two conversation-memory mechanisms.

### Buffer Memory

Stores recent raw conversation messages.

### Summary Memory

Compresses older conversation history into a summary when the buffer exceeds a configured threshold.

The `ContextManager` combines:

```text
System Prompt
+
Conversation Summary
+
Recent Messages
+
Current User Message
```

before sending the request to the model.

## Planning

The project also includes a planning and reasoning workflow.

```text
Task
 |
 v
Planner
 |
 v
Steps
 |
 v
Executor
 |
 v
Agent + Tools
 |
 v
Reflection
 |
 v
Final Synthesis
```

The planner decomposes complex tasks into smaller steps.

The executor performs each step and uses a reflection stage to determine whether a retry is required.

## Setup

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project:

```bash
python -m pip install -e ".[dev]"
```

If build isolation causes dependency-resolution problems:

```bash
python -m pip install -e ".[dev]" --no-build-isolation
```

## Environment Variables

Create a `.env` file:

```text
OPENROUTER_API_KEY=your_key_here
BAI_API_KEY=your_key_here

CHAT_MODEL=openai/gpt-4o-mini
EMBED_MODEL=nvidia/nemotron-3-embed-1b:free
```

Never commit `.env` or API keys to Git.

## Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

Run the portfolio-focused tests:

```bash
python -m pytest \
  tests/test_agent_tools.py \
  tests/test_memory.py \
  tests/test_multi_agent.py \
  -v
```

The test suite validates:

- Tool selection
- Retrieval behavior
- Memory
- Context construction
- Multi-agent communication
- Shared state
- Error handling
- Final answer propagation

Most architecture tests use fake models and mocked external services so they do not depend on an external LLM provider.

## Running the Multi-Agent Pipeline

When the configured LLM provider is available:

```bash
python -c "from agents.manager import run_multi_agent; print(run_multi_agent('Write a report about paper.pdf'))"
```

Expected workflow:

```text
Manager: Delegating research

Researcher
  -> rag_search

Manager: Delegating writing

Writer
  -> draft

Manager: Delegating review

Reviewer
  -> feedback

Manager: Delegating revision

Writer
  -> final response
```

## Example Use Cases

### Document Research

```text
Summarize paper.pdf
```

### Multi-Agent Report

```text
Write a report about paper.pdf
```

### Web Research

```text
Research the latest developments in Python.
```

### Calculation

```text
Calculate 25 multiplied by 4.
```

## Testing Strategy

The project separates architecture tests from external-provider integration.

### Unit and Workflow Tests

These use fake models and deterministic test doubles.

They validate project logic without requiring OpenRouter, Hugging Face, or live web access.

### Integration Tests

These verify real model and provider behavior when external services are available.

This separation prevents provider outages from being confused with application bugs.

## Technology Stack

- Python
- LangChain
- OpenAI-compatible APIs
- OpenRouter
- ChromaDB
- Sentence Transformers
- CrossEncoder
- BM25
- PyPDF
- DDGS
- Pytest
- Pydantic Settings

## What This Project Demonstrates

This repository demonstrates the progression from a basic LLM application to a modular agentic system:

```text
LLM
 ↓
Tools
 ↓
Tool-Using Agent
 ↓
Agentic RAG
 ↓
Memory
 ↓
Planning
 ↓
Reusable Agent Architecture
 ↓
Role-Based Agents
 ↓
Multi-Agent Workflow
```

The final architecture separates responsibilities between agents and keeps tools, prompts, memory, retrieval, planning, and orchestration modular.

## Current Limitations

- External model execution depends on provider availability.
- Retrieval quality depends on the indexed document and embedding model.
- The current multi-agent workflow is sequential.
- Workflow state is in-memory and is not persisted between application runs.
- Reviewer feedback currently triggers one revision pass.

These areas can be extended with persistent state, conditional workflows, parallel agents, structured outputs, observability, and evaluation pipelines.

## Future Improvements

Possible next steps:

- LangGraph-based orchestration
- Persistent workflow state
- Long-term memory
- Structured agent outputs
- Parallel research agents
- Conditional routing
- Multiple reviewer iterations
- Human-in-the-loop approval
- Agent evaluation
- Tracing and observability
- API and web interface

## Status

The project currently includes:

```text
Tool-Using Agent        ✅
Agentic RAG             ✅
Hybrid Retrieval        ✅
Reranking               ✅
Memory                   ✅
Context Management       ✅
Planning                 ✅
Reflection               ✅
Reusable BaseAgent       ✅
Tool Injection           ✅
Role-Based Agents        ✅
Agent Delegation         ✅
Shared Workflow State    ✅
Error Handling           ✅
Multi-Agent Pipeline     ✅
Automated Tests          ✅
Documentation            ✅
```