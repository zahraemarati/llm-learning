from langchain_openai import ChatOpenAI
from config import settings


model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=settings.openrouter_api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0
)


response = model.invoke(
    "Explain RAG in one sentence"
)


print(response.content)