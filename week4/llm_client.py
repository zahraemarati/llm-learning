from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from config import settings


chat_client = ChatOpenAI(
    model=settings.chat_model,
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)


embedding_client = OpenAIEmbeddings(
    model=settings.embed_model,
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)


# backward compatibility
model = chat_client