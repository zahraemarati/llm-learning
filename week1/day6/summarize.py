from openai import OpenAI
from config import settings

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)

def summarize_text(text: str, max_sentences: int = 3) -> str:
    prompt = (
        f"متن زیر را در حداکثر {max_sentences} جمله و به زبان فارسی خلاصه کن. "
        f"فقط خلاصه را برگردان، بدون مقدمه:\n\n{text}"
    )
    response = client.chat.completions.create(
        model=settings.chat_model,
        messages=[{"role": "user", "content": prompt}],
    )
    result = response.choices[0].message.content.strip()
    if len(result) < 15 or "safety" in result.lower():
        raise ValueError(f"خروجی مدل معتبر به نظر نمی‌رسه: {result!r}")
    return result

def summarize_conversation(messages: list[dict]) -> str:
    real_messages = [m for m in messages if m["role"] != "system"]
    if not real_messages:
        return "هنوز مکالمه‌ای برای خلاصه کردن وجود نداره."
    conversation_text = "\n".join(f"{m['role']}: {m['content']}" for m in real_messages)
    return summarize_text(conversation_text, max_sentences=4)