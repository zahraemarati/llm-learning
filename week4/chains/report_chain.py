from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from prompts.report_prompt import report_prompt
from config import settings


model = ChatOpenAI(
    model=settings.chat_model,
    api_key=settings.bai_api_key,
    base_url="https://api.b.ai/v1",
    temperature=0,
)


report_chain = (
    report_prompt
    | model
    | StrOutputParser()
)


if __name__ == "__main__":

    content = """
Retrieval Augmented Generation combines information retrieval
with large language models.

A RAG system retrieves relevant external documents before
generating an answer and provides those documents to the model
as context.

Hybrid retrieval can improve retrieval quality by combining
semantic vector search with lexical methods such as BM25.

Reranking can then reorder retrieved documents based on their
relevance to the user query.
"""

    response = report_chain.invoke(
        {
            "content": content
        }
    )

    print(response)