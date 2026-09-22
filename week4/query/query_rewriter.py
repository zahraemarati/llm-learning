from llm_client import chat_client


class QueryRewriter:

    def rewrite(self, query: str) -> str:

        prompt = f"""
You are a query rewriting assistant.

Rewrite the following user query so that it is
clearer and more suitable for document retrieval.

Return only the rewritten query.
Do not add explanations.

User Query:
{query}

Rewritten Query:
"""

        response = chat_client.invoke(prompt)

        return response.content.strip()