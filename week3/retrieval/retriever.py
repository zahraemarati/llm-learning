from typing import Any
import chromadb
from embeddings.embedder import get_embedding


CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "pdf_documents"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


def retrieve(
    query: str,
    n_results: int = 3,
    where: dict[str, Any] | None = None,
):
    """
    Semantic retrieval with optional Chroma metadata filtering.

    Examples:
        retrieve("question")
            -> searches the whole collection

        retrieve(
            "question",
            where={"page": {"$gte": 10}},
        )
            -> searches only page 10 and later
    """

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    query_embedding = get_embedding(query)

    query_params: dict[str, Any] = {
        "query_embeddings": [
            query_embedding
        ],
        "n_results": n_results,
    }

    if where is not None:
        query_params["where"] = where

    results = collection.query(
        **query_params
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved_chunks = []

    for doc, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        retrieved_chunks.append(
            {
                "text": doc,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return retrieved_chunks
