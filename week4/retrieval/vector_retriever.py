import chromadb

from config import settings
from embeddings.embedder import get_embedding


class VectorRetriever:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=settings.chroma_path
        )

        self.collection = self.client.get_collection(
            name=settings.collection_name
        )


    def retrieve(
        self,
        query: str,
        n_results: int = 5,
        where=None
    ):

        query_embedding = get_embedding(query)


        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=n_results,
            where=where
        )


        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]


        retrieved = []


        for doc, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            score = 1 - distance


            retrieved.append(
                {
                    "text": doc,
                    "metadata": metadata,
                    "score": score,
                    "distance": distance
                }
            )


        return retrieved



_default_retriever = None


def retrieve(
    query: str,
    n_results: int = 5,
    where=None
):

    global _default_retriever


    if _default_retriever is None:
        _default_retriever = VectorRetriever()


    return _default_retriever.retrieve(
        query,
        n_results=n_results,
        where=where
    )