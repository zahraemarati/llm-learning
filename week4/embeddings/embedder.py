from llm_client import embedding_client
from config import settings


def get_embedding(text: str) -> list[float]:
    """Create an embedding for a single text (used for user queries)."""

    response = embedding_client.embeddings.create(
        model=settings.embed_model,
        input=text,
        encoding_format="float",
    )

    return response.data[0].embedding


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Create embeddings for multiple texts in one API request."""

    if not texts:
        return []

    response = embedding_client.embeddings.create(
        model=settings.embed_model,
        input=texts,
        encoding_format="float",
    )

    # Keep output aligned with the original input order.
    ordered_data = sorted(
        response.data,
        key=lambda item: item.index,
    )

    return [
        item.embedding
        for item in ordered_data
    ]
