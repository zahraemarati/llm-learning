from llm_client import chat_client
from config import settings


def generate_answer(
    question: str,
    contexts: list[str]
):

    context_text = "\n\n".join(contexts)


    prompt = f"""
You are a PDF assistant.

Rules:
1. Answer only using the provided context.
2. Do not use outside knowledge.
3. If the answer is not in the context, say:
   "I couldn't find this information in the document."

Context:
{context_text}


Question:
{question}


Answer:
"""


    response = chat_client.chat.completions.create(
        model=settings.chat_model,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.choices[0].message.content