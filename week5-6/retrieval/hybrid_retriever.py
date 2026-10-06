import re

import chromadb
from rank_bm25 import BM25Okapi

from config import settings
from llm_client import embedding_client


def embed_query(query: str) -> list[float]:
    response = embedding_client.embeddings.create(
        model=settings.embed_model,
        input=query,
    )

    return response.data[0].embedding


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def get_collection():
    client = chromadb.PersistentClient(
        path=settings.chroma_path,
    )

    return client.get_or_create_collection(
        name=settings.collection_name,
    )


def vector_search(
    query: str,
    top_k: int = 5,
    source: str | None = None,
) -> list[dict]:
    collection = get_collection()

    if collection.count() == 0:
        return []

    query_embedding = embed_query(query)

    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": [
            "documents",
            "metadatas",
            "distances",
        ],
    }

    if source:
        query_args["where"] = {
            "source": source,
        }

    results = collection.query(**query_args)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    ids = results["ids"][0]

    output = []

    for document_id, document, metadata in zip(
        ids,
        documents,
        metadatas,
    ):
        output.append(
            {
                "id": document_id,
                "content": document,
                "metadata": metadata,
            }
        )

    return output


def keyword_search(
    query: str,
    top_k: int = 5,
    source: str | None = None,
) -> list[dict]:
    collection = get_collection()

    if collection.count() == 0:
        return []

    get_args = {
        "include": [
            "documents",
            "metadatas",
        ]
    }

    if source:
        get_args["where"] = {
            "source": source,
        }

    results = collection.get(**get_args)

    documents = results["documents"]
    metadatas = results["metadatas"]
    ids = results["ids"]

    if not documents:
        return []

    tokenized_documents = [
        tokenize(document)
        for document in documents
    ]

    bm25 = BM25Okapi(
        tokenized_documents
    )

    query_tokens = tokenize(query)

    scores = bm25.get_scores(
        query_tokens
    )

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda index: scores[index],
        reverse=True,
    )[:top_k]

    output = []

    for index in ranked_indices:
        output.append(
            {
                "id": ids[index],
                "content": documents[index],
                "metadata": metadatas[index],
            }
        )

    return output


def merge_results(
    vector_results: list[dict],
    keyword_results: list[dict],
    top_k: int = 5,
) -> list[dict]:
    scores = {}
    documents = {}

    for rank, document in enumerate(
        vector_results,
        start=1,
    ):
        document_id = document["id"]

        documents[document_id] = document

        scores[document_id] = (
            scores.get(document_id, 0)
            + 1 / (60 + rank)
        )

    for rank, document in enumerate(
        keyword_results,
        start=1,
    ):
        document_id = document["id"]

        documents[document_id] = document

        scores[document_id] = (
            scores.get(document_id, 0)
            + 1 / (60 + rank)
        )

    ranked_ids = sorted(
        scores,
        key=scores.get,
        reverse=True,
    )

    return [
        documents[document_id]
        for document_id in ranked_ids[:top_k]
    ]


def hybrid_search(
    query: str,
    top_k: int = 5,
    source: str | None = None,
) -> list[dict]:
    candidate_count = top_k * 2

    vector_results = vector_search(
        query=query,
        top_k=candidate_count,
        source=source,
    )

    keyword_results = keyword_search(
        query=query,
        top_k=candidate_count,
        source=source,
    )

    return merge_results(
        vector_results=vector_results,
        keyword_results=keyword_results,
        top_k=top_k,
    )