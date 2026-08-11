from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

response = client.chat.completions.create(
    model="llama3:latest",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful programming teacher. Answer simply."
        },
        {
            "role": "user",
            "content": "My name is Zahra and I am learning Python."
        },
        {
            "role": "assistant",
            "content": "Nice to meet you, Zahra! I'll help you learn Python."
        },
        {
            "role": "user",
            "content": "What is my name and what am I learning?"
        }
    ]
)
print(response.choices[0].message.content)