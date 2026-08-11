import os

import httpx
from dotenv import load_dotenv
from openai import (
    OpenAI,
    APIConnectionError,
    APITimeoutError,
    APIStatusError,
)

from prompts import SYSTEM_PROMPT


load_dotenv()


MODEL = os.getenv("LLM_MODEL", "llama3:latest")
BASE_URL = os.getenv(
    "LLM_BASE_URL",
    "http://127.0.0.1:11434/v1/"
)
API_KEY = os.getenv("LLM_API_KEY", "ollama")


client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    max_retries=0,
    http_client=httpx.Client(
        trust_env=False
    ),
)


class LLMError(Exception):
    pass


def ask_llm(user_message: str) -> str:

    if not user_message.strip():
        raise ValueError("پیام نمی‌تواند خالی باشد.")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise LLMError("مدل پاسخ خالی برگرداند.")

        return content.strip()

    except APITimeoutError as error:
        raise LLMError(
            "زمان پاسخ مدل بیش از حد طول کشید."
        ) from error

    except APIConnectionError as error:
        raise LLMError(
            "اتصال به مدل برقرار نشد."
        ) from error

    except APIStatusError as error:
        raise LLMError(
            f"مدل خطای HTTP {error.status_code} برگرداند."
        ) from error