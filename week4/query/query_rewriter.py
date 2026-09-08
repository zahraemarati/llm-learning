from llm_client import chat_client
from config import settings


class QueryRewriter:

    def rewrite(self, question: str) -> str:

        response = chat_client.chat.completions.create(
            model=settings.chat_model,
            messages=[
                {
                    "role": "user",
                    "content": f"""
Rewrite the user question into a better search query.

The query will be used for document retrieval.

Return only the improved search query.

Question:
{question}
"""
                }
            ],
        )

        return response.choices[0].message.content.strip()