from retrievers.hybrid_retriever import LangChainHybridRetriever


def test_hybrid_retriever_returns_documents():

    retriever = LangChainHybridRetriever(
        candidate_k=10,
        top_k=5,
    )

    query = (
        "What are the major development trends "
        "of intelligent technologies?"
    )

    documents = retriever.invoke(query)

    assert documents is not None

    assert len(documents) > 0

    document = documents[0]

    assert document.page_content

    assert isinstance(
        document.metadata,
        dict
    )