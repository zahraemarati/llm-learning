import time
from openai import OpenAI, RateLimitError
from config import settings

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)

def chat_complete(messages: list[dict], retries: int = 3, delay: int = 5) -> str:
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=settings.chat_model,
                messages=messages,
            )
            return response.choices[0].message.content
        except RateLimitError:
            if attempt == retries - 1:
                raise
            print(f"مدل موقتاً شلوغه، تلاش دوباره ({attempt + 1}/{retries}) تا {delay} ثانیه دیگر...")
            time.sleep(delay)