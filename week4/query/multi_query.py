import re

from llm_client import chat_client


class MultiQueryGenerator:

    def generate(
        self,
        query: str,
        number_of_queries: int = 3,
    ) -> list[str]:

        prompt = f"""
You are a search query generation assistant.

Generate {number_of_queries} alternative search queries
for the following question.

The queries should preserve the original meaning
but use different wording to improve retrieval.

Return one query per line.
Do not provide explanations.

Original Query:
{query}

Alternative Queries:
"""

        response = chat_client.invoke(prompt)

        content = response.content.strip()

        queries = []

        for line in content.splitlines():

            line = line.strip()

            if not line:
                continue

            # Remove formats such as:
            # 1. query
            # 2) query
            # - query
            line = re.sub(
                r"^\s*(?:\d+[\.\)]|[-*])\s*",
                "",
                line,
            )

            if line:
                queries.append(line)

        return queries[:number_of_queries]