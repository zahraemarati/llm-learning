from llm_client import client
from config import settings


def generate_answer(
    question: str,
    contexts: list[str]
):

    context_text = "\n\n".join(contexts)


    prompt = f"""
You are an AI assistant that answers questions using only the provided context.

Rules:
- Do not use outside knowledge.
- If the answer is not available in the context, say that you cannot find it.
- Keep the answer clear and concise.

Context:
{context_text}


Question:
{question}


Answer:
"""


    response = client.chat.completions.create(
        model=settings.chat_model,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.choices[0].message.content