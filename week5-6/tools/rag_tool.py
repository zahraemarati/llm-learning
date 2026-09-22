import chromadb
from langchain_core.tools import tool

from config import settings
from llm_client import embedding_client


def embed_query(query: str) -> list[float]:
    response = embedding_client.embeddings.create(
        model=settings.embed_model,
        input=query,
    )

    return response.data[0].embedding


@tool
def rag_search(query: str) -> str:
    """
    Search the local knowledge base for relevant information.

    Use this tool when the user asks a question that may be answered
    using documents stored in the local vector database.
    """

    client = chromadb.PersistentClient(
        path=settings.chroma_path,
    )

    collection = client.get_or_create_collection(
        name=settings.collection_name,
    )

    if collection.count() == 0:
        return "The knowledge base is empty."

    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0]

    if not documents:
        return "No relevant documents were found."

    return "\n\n".join(documents)