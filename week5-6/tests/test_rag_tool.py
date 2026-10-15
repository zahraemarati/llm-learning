import tools.rag_tool as rag_tool_module


def test_rag_search_returns_string(
    monkeypatch,
):
    fake_documents = [
        {
            "id": "doc-1",
            "content": "RAG combines retrieval and generation.",
            "metadata": {
                "source": "paper.pdf",
                "page": 1,
            },
        }
    ]

    monkeypatch.setattr(
        rag_tool_module,
        "hybrid_search",
        lambda query, top_k=10, source=None: fake_documents,
    )

    monkeypatch.setattr(
        rag_tool_module,
        "rerank_documents",
        lambda query, documents, top_k=3: documents,
    )

    result = rag_tool_module.rag_search.invoke(
        {
            "query": "What is RAG?",
            "source": "paper.pdf",
        }
    )

    assert isinstance(
        result,
        str,
    )

    assert "RAG" in result