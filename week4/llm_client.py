from openai import OpenAI
from config import settings


embedding_client = OpenAI(
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1"
)

chat_client = OpenAI(
    api_key=settings.bai_api_key,
    base_url="https://api.b.ai/v1"
)