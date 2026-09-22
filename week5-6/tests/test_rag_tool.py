from tools.rag_tool import rag_search


def test_rag_search_returns_string():
    result = rag_search.invoke(
        {
            "query": "What is RAG?",
        }
    )

    assert isinstance(result, str)