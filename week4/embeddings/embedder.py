from llm_client import embedding_client
from config import settings


def get_embedding(text: str) -> list[float]:

    response = embedding_client.embeddings.create(
        model=settings.embed_model,
        input=text,
    )

    return response.data[0].embedding



def get_embeddings(texts: list[str]) -> list[list[float]]:

    if not texts:
        return []

    response = embedding_client.embeddings.create(
        model=settings.embed_model,
        input=texts,
    )

    return [
        item.embedding
        for item in response.data
    ]