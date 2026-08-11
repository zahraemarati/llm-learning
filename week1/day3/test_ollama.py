import httpx
from openai import OpenAI


client = OpenAI(
    base_url="http://127.0.0.1:11434/v1/",
    api_key="ollama",
    max_retries=0,
    http_client=httpx.Client(trust_env=False),
)


response = client.chat.completions.create(
    model="llama3:latest",
    messages=[
        {
            "role": "user",
            "content": "hello"
        }
    ],
)


print(response.choices[0].message.content)