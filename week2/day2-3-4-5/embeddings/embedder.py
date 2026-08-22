from llm_client import client
from config import settings


def get_embedding(text: str):

    response = client.embeddings.create(
        model=settings.embed_model,
        input=text,
        encoding_format="float"
    )

    return response.data[0].embedding