import chromadb

from embeddings.embedder import get_embedding

client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_collection(
    name="pdf_documents"
)


def retrieve(query: str, n_results: int = 3):

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=n_results
    )


    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]


    retrieved_chunks = []

    for doc, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        retrieved_chunks.append(
            {
                "text": doc,
                "metadata": metadata,
                "distance": distance
            }
        )


    return retrieved_chunks