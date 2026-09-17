from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from config import settings
from prompts.rag_prompt import rag_prompt
from retrievers.hybrid_retriever import LangChainHybridRetriever


model = ChatOpenAI(
    model=settings.chat_model,
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)


retriever = LangChainHybridRetriever(
    candidate_k=10,
    top_k=5,
)


answer_chain = (
    rag_prompt
    | model
    | StrOutputParser()
)


def format_documents(documents):

    return "\n\n".join(
        document.page_content
        for document in documents
    )


def extract_sources(documents):

    sources = []

    for document in documents:

        source_info = {
            "source": document.metadata.get(
                "source",
                "Unknown source",
            ),
            "page": document.metadata.get("page"),
        }

        if source_info not in sources:
            sources.append(source_info)

    return sources


def ask_rag(question: str):

    documents = retriever.invoke(question)

    context = format_documents(documents)

    answer = answer_chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )

    sources = extract_sources(documents)

    return {
        "answer": answer,
        "sources": sources,
    }


if __name__ == "__main__":

    question = (
        "What are the major development trends "
        "of intelligent technologies?"
    )

    result = ask_rag(question)

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nSources:")

    for index, source in enumerate(
        result["sources"],
        start=1,
    ):
        print(
            f"{index}. "
            f"{source['source']} "
            f"- page {source['page']}"
        )