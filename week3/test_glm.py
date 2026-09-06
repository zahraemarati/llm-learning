from llm_client import chat_client
from config import settings


response = chat_client.chat.completions.create(
    model=settings.chat_model,
    messages=[
        {
            "role": "user",
            "content": "Explain RAG in one sentence."
        }
    ]
)


print(response.choices[0].message.content)