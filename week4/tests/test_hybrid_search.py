from retrieval.hybrid_retriever import HybridRetriever


retriever = HybridRetriever()


def test_hybrid_search():

    results = retriever.retrieve(
        "artificial intelligence"
    )

    assert len(results) > 0


    for r in results:
        print(
            r["metadata"],
            r["score"],
            r["text"][:100]
        )


def test_bm25_keyword():

    results = retriever.retrieve(
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