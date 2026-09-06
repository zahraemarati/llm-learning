# Week 3 - Day 2: Metadata Filtering + Batch Embeddings

Replace these files in the project while preserving the same folder structure:

- `embeddings/embedder.py`
- `vector_store/chroma_db.py`
- `retrieval/retriever.py`
- `rag_pipeline.py`
- `tests/test_metadata_filtering.py` (new file)
- `frontend/app.py` (only source page display changes from `page + 1` to `page`)

## Why batch embedding was added

The PDF contains hundreds of chunks and the embedding provider has a requests-per-minute limit. `get_embeddings()` embeds multiple chunks in one API request.

## Metadata contract

```python
{
    "page": 10,
    "source": "paper.pdf",
}
```

Page numbers are stored as **1-based** values.

## Search the entire PDF

```python
retrieve(
    "What is Artificial Intelligence?",
    n_results=10,
)
```

## Search only page 10 and later

```python
retrieve(
    "What is Artificial Intelligence?",
    n_results=10,
    where={
        "page": {
            "$gte": 10
        }
    },
)
```

## Search only pages 10 through 20

```python
retrieve(
    "What is Artificial Intelligence?",
    n_results=10,
    where={
        "$and": [
            {"page": {"$gte": 10}},
            {"page": {"$lte": 20}},
        ]
    },
)
```

## Rebuild Chroma on macOS

Run from the project root:

```bash
rm -rf chroma_db
source .venv/bin/activate
python -c "from vector_store.chroma_db import create_vector_store; print(create_vector_store('uploads/paper.pdf'))"
```

Then run the test:

```bash
python -m pytest -s tests/test_metadata_filtering.py
```
