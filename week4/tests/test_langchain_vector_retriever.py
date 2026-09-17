from langchain_core.documents import Document

from retrievers.vector_retriever import (
    LangChainVectorRetriever,
)


def test_vector_retriever():

    retriever = LangChainVectorRetriever(
        k=3
    )

    documents = retriever.invoke(
        "What is artificial intelligence?"
    )

    assert len(documents) <= 3

    assert all(
        isinstance(doc, Document)
        for doc in documents
    )