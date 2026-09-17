from langchain_core.documents import Document

from retrievers.hybrid_retriever import (
    LangChainHybridRetriever,
)


def test_langchain_hybrid_retriever():

    retriever = LangChainHybridRetriever(
        candidate_k=10,
        top_k=3,
    )

    documents = retriever.invoke(
        "What are the major trends in intelligent technologies?"
    )

    assert len(documents) <= 3

    assert all(
        isinstance(doc, Document)
        for doc in documents
    )

    for doc in documents:
        assert "rerank_score" in doc.metadata