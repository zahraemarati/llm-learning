import chromadb

from config import settings
from embeddings.embedder import get_embedding


client = chromadb.PersistentClient(
    path=settings.chroma_path
)


collection = client.get_collection(
    name=settings.collection_name
)


def retrieve(
    query: str,
    n_results: int = 5,
    where=None
):

    query_embedding = get_embedding(query)


    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where
    )


    documents = results["documents"][0]
    metadatas = results["metadatas"][0]


    return [
        {
            "text": doc,
            "metadata": metadata
        }
        for doc, metadata in zip(
            documents,
            metadatas
        )
    ]