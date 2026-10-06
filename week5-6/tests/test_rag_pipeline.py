from context.context_builder import build_context
from retrieval.reranker import rerank_documents


def test_reranker_and_context_builder():

    documents = [
        {
            "content": "Attention is used in transformer models.",
            "metadata": {
                "source": "paper.pdf"
            },
        },
        {
            "content": "RAG combines retrieval and generation.",
            "metadata": {
                "source": "rag.pdf"
            },
        },
    ]

    ranked_documents = rerank_documents(
        "What is attention?",
        documents,
    )

    context = build_context(
        ranked_documents
    )

    assert isinstance(context, str)
    assert len(context) > 0