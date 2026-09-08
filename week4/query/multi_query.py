from llm_client import chat_client
from config import settings


class MultiQueryGenerator:

    def generate(
        self,
        question: str,
        number_of_queries: int = 3,
    ):

        response = chat_client.chat.completions.create(
            model=settings.chat_model,
            messages=[
                {
                    "role": "user",
                    "content": f"""
Generate {number_of_queries} different search queries
for the following question.

Each query should cover a different perspective.

Return only queries.
Each query must be on a new line.

Question:
{question}
"""
                }
            ],
        )

        queries = [
            query.strip()
            for query in response.choices[0].message.content.split("\n")
            if query.strip()
        ]

        return queries[:number_of_queries]