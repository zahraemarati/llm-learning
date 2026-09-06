from retrieval.hybrid_retriever import hybrid_retrieve


def test_hybrid_search():

    results = hybrid_retrieve(
        "artificial intelligence"
    )

    assert len(results) > 0

    for r in results:
        print(
            r["metadata"],
            r["text"][:100]
        )

def test_bm25_keyword():

    results = hybrid_retrieve(
        "PyTorch"
    )

    texts = [
        r["text"]
        for r in results
    ]

    assert any(
        "PyTorch" in text
        for text in texts
    )