from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from prompts.qa_prompt import qa_prompt
from config import settings


model = ChatOpenAI(
    model=settings.chat_model,
    api_key=settings.bai_api_key,
    base_url="https://api.b.ai/v1",
    temperature=0,
)


qa_chain = (
    qa_prompt
    | model
    | StrOutputParser()
)


if __name__ == "__main__":

    context = """
Retrieval Augmented Generation combines information retrieval
with large language models.

Before generating an answer, the system retrieves relevant
documents and provides them to the language model as context.

This can reduce hallucination and allows the model to answer
questions using private or updated information.
"""

    question = "Why is RAG useful?"

    response = qa_chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    print(response)